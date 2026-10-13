"""One internal clock -> 4-clock/16-byte keystream blocks -> byte stream."""
from .context import StreamContext
from .core.fsm import fsm_step
from .core.lfsr import lfsr_step
from .core.word32 import store32le
from .output_transform import output_transform

def clock(ctx: StreamContext) -> tuple[int,int]:
    """Produce (discarded_word, f_t); update FSM from OLD LFSR, then LFSR."""
    r1,r2,f = fsm_step(ctx.r1,ctx.r2,ctx.s)
    dropped = lfsr_step(ctx.s)
    ctx.r1,ctx.r2 = r1,r2
    return dropped, f

def generate_block(ctx: StreamContext) -> bytes:
    """Generate 16 NEW bytes. Call generate() for byte-stream semantics."""
    values=[clock(ctx) for _ in range(4)]
    dropped,fvalues=zip(*values)
    words=output_transform(list(fvalues),list(dropped))
    return b''.join(store32le(w) for w in words)

def generate(ctx: StreamContext, size: int) -> bytes:
    """Sequential keystream; preserves unused bytes of a 16-byte block."""
    if size < 0:
        raise ValueError('size must be non-negative')
    out=bytearray()
    while len(out)<size:
        if ctx.buffer_pos >= len(ctx.buffer):
            ctx.buffer=generate_block(ctx)
            ctx.buffer_pos=0
        count=min(size-len(out),len(ctx.buffer)-ctx.buffer_pos)
        out.extend(ctx.buffer[ctx.buffer_pos:ctx.buffer_pos+count])
        ctx.buffer_pos+=count
    return bytes(out)
