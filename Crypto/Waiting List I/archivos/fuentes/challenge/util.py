from Crypto.Util.number import isPrime, getPrime, bytes_to_long, long_to_bytes

# Simula una caché donde se almacenan partes intermedias de la firma CRT
class MEMORY:
    def __init__(self):
        self.cache = {}

    def load(self, m):
        return self.cache.get(m, [None, None])

    def store(self, m, sp, sq):
        self.cache[m] = [sp, sq]

    def reset(self, m, slot):
        if m in self.cache:
            self.cache[m][slot] = None

# Implementación de RSA-CRT con caché para firmas
class RSA:
    def __init__(self, memory):
        self.memory = memory
        self.keygen()

    def keygen(self, bits = 2048):
        e = 0x10001
        p = getPrime(bits // 2)
        q = self.next_prime(p)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)

        # Precomputaciones para optimizar firma (CRT)
        dp = d % (p - 1)
        dq = d % (q - 1)
        q_inv = pow(q, -1, p)

        self.public_key = (e, n)
        self.private_key = (dp, dq, q_inv, p, q)

    def next_prime(self, n):
        # Retorna el siguiente número primo estrictamente mayor a n.
        candidate = n + 1 if n % 2 == 0 else n + 2
        while not isPrime(candidate):
            candidate += 2
        return candidate

    def sign(self, message):
        dp, dq, q_inv, p, q = self.private_key
        m = bytes_to_long(message)

        sp, sq = self.cache_signature(m, dp, dq, p, q)
        h = (q_inv * (sp - sq)) % p
        return sq + h * q

    def cache_signature(self, m, dp, dq, p, q):
        sp, sq = self.memory.load(m)

        if sp is None:
            sp = pow(m, dp, p)
        if sq is None:
            sq = pow(m, dq, q)

        self.memory.store(m, sp, sq)
        return sp, sq

    def verify(self, message, s):
        e, n = self.public_key
        m = pow(s, e, n)
        return long_to_bytes(m) == message

    def reset_cache(self, message, slot):
        m = bytes_to_long(message)
        self.memory.reset(m, slot)