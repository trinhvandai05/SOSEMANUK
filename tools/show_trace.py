"""Print intermediate values to compare with the authors' reference trace."""
import argparse
from sosemanuk.key_setup import key_setup
from sosemanuk.serpent.serpent24 import serpent24
from sosemanuk.iv_setup import map_initial_state
from sosemanuk.keystream import clock

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--key',default='a7c083feb7',help='key hex')
    p.add_argument('--iv',default='00112233445566778899aabbccddeeff',help='IV hex')
    args=p.parse_args()
    kc=key_setup(bytes.fromhex(args.key))
    for i,k in enumerate(kc.subkeys):
        print(f'K{i:02}: '+' '.join(f'{v:08X}' for v in reversed(k)))
    cp=serpent24(bytes.fromhex(args.iv),kc.subkeys)
    for n in (12,18,24):
        print(f'Y{n}: '+' '.join(f'{v:08X}' for v in reversed(cp[n])))
    ctx=map_initial_state(cp)
    print('LFSR initial:',*[f'{v:08X}' for v in ctx.s])
    print(f'FSM initial R1={ctx.r1:08X} R2={ctx.r2:08X}')
    for i in range(8):
        dropped,f=clock(ctx)
        print(f'clock {i+1}: dropped={dropped:08X} f={f:08X} '
              f'R1={ctx.r1:08X} R2={ctx.r2:08X} new={ctx.s[-1]:08X}')

if __name__=='__main__': main()
