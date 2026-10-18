"""Extract independently generated SOSEMANUK trace from author's C stdout.

Not a keystream implementation; does not derive expected output from Python code.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

HEX = r"([0-9A-Fa-f]{8})"
RE_KEY = re.compile(r"^key\s*=\s*([0-9a-fA-F]+)\s*$", re.I)
RE_IV = re.compile(r"^IV\s*=\s*([0-9a-fA-F]+)\s*$")
RE_SUBKEY = re.compile(r"^Serpent24 subkey\s+(\d+):\s*" + r"\s+".join([HEX]*4), re.I)
RE_INITIAL = re.compile(r"^s(10|[1-9])\s*=\s*" + HEX + r"$", re.I)
RE_FSM_INIT = re.compile(r"^Initial FSM state:\s*r1\s*=\s*" + HEX + r"\s+r2\s*=\s*" + HEX, re.I)
RE_FSM = re.compile(r"^New FSM state:\s*r1\s*=\s*" + HEX + r"\s+r2\s*=\s*" + HEX, re.I)
RE_DROP = re.compile(r"^dropped\s*\(s_t\):\s*" + HEX, re.I)
RE_LFSR = re.compile(r"^s_t\+(\d+)\s*=\s*" + HEX + r"$", re.I)
RE_F = re.compile(r"^Intermediate output:\s*" + HEX, re.I)
RE_SERPENT = re.compile(r"^Serpent1 (input|output):\s*" + r"\s+".join([HEX]*4), re.I)
RE_STREAM = re.compile(r"^Stream output:\s*([0-9a-fA-F]{32})", re.I)

def parse_one(text, source_url, sha):
    # Select a detailed test-vector section, not stdout containing both vectors.
    keymatch=list(RE_KEY.finditer(text))  # Each line is matched via MULTILINE below instead.
    sections=re.split(r'(?=^key\s*=\s*[0-9a-fA-F]+\s*$)', text, flags=re.M)
    sections=[s for s in sections if re.search(r'^key\s*=',s,flags=re.M)]
    if not sections:
        raise ValueError('No C SOSEMANUK_VECTOR detailed test vectors found')
    parsed=[]
    for section in sections:
        lines=section.splitlines()
        key=iv=None
        subs={}; si={}; r0=None; clocks=[]; pending={}; serpent_blocks=[]; block={}; outputs=[]
        in_initial=False
        for raw in lines:
            line=raw.strip()
            if not line: continue
            m=RE_KEY.fullmatch(line)
            if m: key=m.group(1).lower();continue
            m=RE_IV.fullmatch(line)
            if m: iv=m.group(1).lower();continue
            m=RE_SUBKEY.match(line)
            if m:
                idx=int(m.group(1));subs[idx]=list(reversed([int(v,16) for v in m.groups()[1:]]));continue
            if line.startswith('Initial LFSR state:'):in_initial=True;continue
            m=RE_INITIAL.fullmatch(line)
            if m and in_initial:si[int(m.group(1))]=int(m.group(2),16);continue
            m=RE_FSM_INIT.match(line)
            if m:r0=[int(m.group(1),16),int(m.group(2),16)];in_initial=False;continue
            m=RE_FSM.match(line)
            if m:
                if pending.get('f') is not None:clocks.append(pending);pending={}
                pending['r1']=int(m.group(1),16);pending['r2']=int(m.group(2),16);continue
            m=RE_DROP.match(line)
            if m:pending['dropped']=int(m.group(1),16);continue
            m=RE_LFSR.match(line)
            if m:
                pending.setdefault('after_s',{})[int(m.group(1))]=int(m.group(2),16);continue
            m=RE_F.match(line)
            if m:
                pending['f']=int(m.group(1),16)
                if 'after_s' in pending:
                    s=pending['after_s'];pending['after_s']=[s[i] for i in sorted(s)]
                clocks.append(pending);pending={}
                continue
            m=RE_SERPENT.match(line)
            if m:
                label=m.group(1).lower()
                block[label]=list(reversed([int(v,16) for v in m.groups()[1:]]))
                if label=='output':serpent_blocks.append(block);block={}
                continue
            m=RE_STREAM.match(line)
            if m:outputs.append(m.group(1).lower());continue
        if not(key and iv and len(subs)==25 and len(si)==10 and r0 and len(clocks)>=8 and len(serpent_blocks)>=2 and len(outputs)>=2):
            raise ValueError('Incomplete C reference log: needs key, IV, 25 subkeys, 12 initial words, >=8 clocks, >=2 Serpent1 blocks, >=2 stream blocks: '
                +repr((key,iv,len(subs),len(si),r0,len(clocks),len(serpent_blocks),len(outputs))))
        if len(clocks)%4:raise ValueError('C trace clocks must come in groups of four')
        if any('after_s' not in c or len(c['after_s'])!=10 or not all(x in c for x in ('r1','r2','dropped','f')) for c in clocks):
            raise ValueError('Malformed FSM/LFSR clock trace')
        parsed.append({'key':key,'iv':iv,'subkeys':[subs[i] for i in range(25)],
                      'initial_state':{'s':[si[i] for i in range(1,11)],'r1':r0[0],'r2':r0[1]},
                      'clocks':clocks,'serpent_blocks':serpent_blocks,'stream_blocks':outputs})
    return {'source_kind':'author_c_stdout_SOSEMANUK_VECTOR','source_url':source_url,
        'raw_stdout_sha256':sha,'vectors':parsed}

def decode_log(data: bytes) -> tuple[str, str]:
    """Decode the raw C log strictly. Windows PowerShell 5.1 '>' writes UTF-16LE
    with a BOM; reading that as UTF-8 silently yields text with NUL bytes."""
    if data.startswith((b'\xff\xfe', b'\xfe\xff')):
        return data.decode('utf-16'), 'utf-16'
    return data.decode('utf-8-sig'), 'utf-8'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--out',required=True)
    p.add_argument('--source-url',default='https://github.com/cchcc/SOSEMANUK/blob/master/C/SOSEMANUK.C')
    args=p.parse_args()
    data=Path(args.input).read_bytes()
    text,encoding=decode_log(data)
    obj=parse_one(text,args.source_url,hashlib.sha256(data).hexdigest())
    obj['raw_stdout_encoding']=encoding
    # Same log captured on Windows/Linux differs only in CRLF/encoding; this hash does not.
    normalized='\n'.join(text.splitlines())+'\n'
    obj['normalized_stdout_sha256']=hashlib.sha256(normalized.encode('ascii')).hexdigest()
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(f'Extracted {len(obj["vectors"])} verified-format C trace(s) to {out}; SHA256={obj["raw_stdout_sha256"]}')
if __name__ == '__main__':main()
