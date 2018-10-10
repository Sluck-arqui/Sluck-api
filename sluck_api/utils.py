def extract_tags(s, division):
    return list(set(
        part[1:] for part in s.split() if part.startswith(division)
    ))
