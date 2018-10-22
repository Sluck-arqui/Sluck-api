def extract_tags(s, division):
    return list(set(
        part[1:] for part in s.split() if part.startswith(division)
    ))


STATUS_CODE_200_DELETE = {'status_text': 'Deleted successfully'}
STATUS_CODE_400 = {'status_text': 'Bad request'}
STATUS_CODE_403 = {'status_text': 'Forbidden action'}
STATUS_CODE_404 = {'status_text': 'Object not found'}
STATUS_CODE_405 = {'status_text': 'Method not allowed'}
STATUS_CODE_498 = {'status_text': 'Invalid oauth_token'}

REACTION_TYPES = {1: 'likes',
                  2: 'dislikes'}
