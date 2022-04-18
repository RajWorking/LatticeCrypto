# LatticeCrypto

for later
```
# server
key = int(''.join(str(i) for i in (np.array(
        list(signers['priv'][i][0]) + list(signers['priv'][i][1])) + 1)), base=3)

# client
key = np.array(list(np.base_repr(key, base=3)), dtype='int')
key = np.pad(key, (f-len(key), 0)) - 1

```