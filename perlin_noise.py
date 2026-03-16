#!/usr/bin/env python3
"""Perlin noise — 2D gradient noise for procedural generation."""
import math,random
def _fade(t):return t*t*t*(t*(t*6-15)+10)
def _lerp(a,b,t):return a+t*(b-a)
def _grad(h,x,y):
    v=x if h&1==0 else y
    return v if h&2==0 else -v
class PerlinNoise:
    def __init__(self,seed=0):
        random.seed(seed)
        self.p=list(range(256));random.shuffle(self.p);self.p*=2
    def noise(self,x,y):
        X=int(math.floor(x))&255;Y=int(math.floor(y))&255
        x-=math.floor(x);y-=math.floor(y)
        u=_fade(x);v=_fade(y)
        A=self.p[X]+Y;B=self.p[X+1]+Y
        return _lerp(_lerp(_grad(self.p[A],x,y),_grad(self.p[B],x-1,y),u),
                     _lerp(_grad(self.p[A+1],x,y-1),_grad(self.p[B+1],x-1,y-1),u),v)
    def octave_noise(self,x,y,octaves=4,persistence=0.5):
        total=0;freq=1;amp=1;max_val=0
        for _ in range(octaves):
            total+=self.noise(x*freq,y*freq)*amp;max_val+=amp
            amp*=persistence;freq*=2
        return total/max_val
def main():
    pn=PerlinNoise(42)
    for y in range(10):
        row="".join("█" if pn.octave_noise(x*0.1,y*0.1)>0 else " " for x in range(40))
        print(row)
if __name__=="__main__":main()
