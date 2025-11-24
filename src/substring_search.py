#-------------------boyer_moore-----------------------------
def boyer_moore(text: str, pattern: str, use_good_suffix=False) -> tuple[int | None, int, int]:
    def build_bad_char_table(pattern: str) -> dict[str, int]:
        bad_char = {}
        for idx, sym in enumerate(pattern):
            # store most right index
            bad_char[sym] = idx

        return bad_char
        
    def build_good_suffix_table(pattern: str) -> list[int]:
        # scanning pattern from right to left
        # searching leftmost suffix and calculate shift
        m = len(pattern)
        # last always = 1
        # default suffix = length of pattern
        gs = ([m] * (m-1)) + [1]
        for i in range(m-2, -1, -1):
            suffix = pattern[i+1:]
            k = m - i - 1
            for j in range(i+1-k, -1, -1):
                # check suffix and we must be at the beggining or first symbol before suffix dont match current symbol
                if pattern[j:j+k] == suffix and (j == 0 or pattern[j-1] != pattern[i]):
                    gs[i] = i - j # variant A: shfit, we found suffix
                    break
            # if we didnt found suffix, looking varian B
            if gs[i] == m:
                while k > 0:
                    if pattern[:k] == suffix[-k:]:
                        gs[i] = max(1, m - k)
                        break
                    k -= 1
        return gs

    if not pattern:
        return 0, 0, 0   

    if len(text) < len(pattern):
        return None, 0, 0             

    bad_char = build_bad_char_table(pattern)
    if use_good_suffix:
        gs = build_good_suffix_table(pattern)       

    m = len(pattern)    
    comparing = 0
    jumps = 0
    window_idx = 0
    while window_idx <= (len(text)-m):
        shift = 0
        for j in range(m-1, -1, -1):
            # moving from end of window to beginning
            comparing += 1
            if text[window_idx+j] != pattern[j]:
                # if not found, jump using bad char table
                bc_shift = max(1, j-bad_char.get(text[window_idx+j], -1))
                if use_good_suffix:
                    # use good char shift and choose best
                    gc_shift = gs[j]
                    shift = max(bc_shift, gc_shift)
                else:
                    shift = bc_shift
                window_idx += shift
                jumps += 1
                break
        if shift == 0:
            # if shift is zero, we found pattern
            return window_idx, comparing, jumps
    return None, comparing, jumps


#-----------------------kmp---------------------------------
def kmp(text: str, pattern: str) -> int | None:

    if not pattern:
        return 0    
    if len(text) < len(pattern):
        return None
    
    def build_LPS(pattern: str) -> list:
        # building LPS list
        lps = [0] * len(pattern)
        m = len(pattern)
        j = 0
        i = 1

        while i < m:
            if pattern[j] == pattern[i]:
                # if match, move next and "remember" in LPS count of total matching
                j += 1
                lps[i] = j
                i += 1
            else:         
                # are we at beginning?       
                if j > 0: 
                    # no, check backward
                    j = lps[j-1]
                else:
                    # yes, start from 0
                    j = 0 
                    lps[i] = 0
                    i += 1
        return lps

    lps = build_LPS(pattern)

    n = len(text)
    m = len(pattern)
    i = 0 # text pointer
    j = 0 # pattern pointer
    while i < n and j < m:
        if pattern[j] == text[i]:
            # "naive search". just move forward
            i += 1
            j += 1
        else:
            # are we at begining?
            if j > 0:            
                # use previous matching part
                j = lps[j-1]
            else:
                # go to the next symbol, start over
                i += 1
    if j == m:
        return i - m
    else:
        return None
        

#-------------------rabin_karp------------------------------
def rabin_karp(text, pattern):

    def hash_window(s):
        h = 0
        for i in range(m):
            h = (h * base + ord(s[i])) % q
        return h

    def rolling_hash(h, left, right):
        h = (h - ord(left) * high) % q
        h = (h * base + ord(right)) % q
        return h

    if not pattern:
        return 0    
    if len(text) < len(pattern):
        return None        

    q = 2 ** 31 - 1 # Mersen
    m = len(pattern)
    n = len(text)
    base = 256
    high = base**(m-1) % q


    pattern_hash = hash_window(pattern)
    window_hash = hash_window(text[:m])
    for i in range(n - m + 1):        
        if pattern_hash == window_hash:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            window_hash = rolling_hash(window_hash,text[i],text[i+m])
    return None

#-----------------------tests--------------------------------

if __name__ == "__main__":
    text = "ABCAABBCAABCBACBACA"
    pattern = "CBACA"

    pos, comparing, jumps = boyer_moore(text,pattern,use_good_suffix=True)

    print(f"Searching '{pattern}' in '{text}'")
    print(f"found at {pos} position")
    print(f"This takes {comparing} comparing and {jumps} jumps")

    text = "ABCAABBCAABCBACBACA"
    pattern = "CBACA"

    pos, comparing, jumps = boyer_moore(text,pattern)

    print(f"Searching '{pattern}' in '{text}'")
    print(f"found at {pos} position")
    print(f"This takes {comparing} comparing and {jumps} jumps")

    text = "AABAAACAAAACBACBACA"
    pattern = "AAACAAAA"
    pos = kmp(text,pattern)

    print(f"Searching '{pattern}' in '{text}'")
    print(f"found at {pos} position")



