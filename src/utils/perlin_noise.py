import numpy as np

def generate_perlin_noise(width, height, seed, scale=10.0, octaves=1, persistence=0.5, lacunarity=2.0):
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(a, b, t):
        return a + t * (b - a)

    def grad(hash, x, y):
        h = hash & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return ((u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v))

    def perlin(x, y):
        xi = int(x) & 255
        yi = int(y) & 255
        xf = x - int(x)
        yf = y - int(y)

        u = fade(xf)
        v = fade(yf)

        aa = p[p[xi] + yi]
        ab = p[p[xi] + yi + 1]
        ba = p[p[xi + 1] + yi]
        bb = p[p[xi + 1] + yi + 1]

        x1 = lerp(grad(aa, xf, yf), grad(ab, xf, yf - 1), v)
        x2 = lerp(grad(ba, xf - 1, yf), grad(bb, xf - 1, yf - 1), v)

        return (lerp(x1, x2, u) + 1) / 2

    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()

    noise = np.zeros((height, width))

    max_amplitude = 0
    amplitude = 1
    frequency = 1

    for _ in range(octaves):
        for y in range(height):
            for x in range(width):
                noise[y][x] += amplitude * perlin(x * frequency / scale, y * frequency / scale)
        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    # Normalize the noise values to the range [0, 1]
    noise = noise / max_amplitude

    return noise