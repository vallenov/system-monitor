from cron import validate_rule


def test_rule_validation():
    good = ['* * * * * * *',
            '*/12 * * * * * *',
            '* 1 * * * * *',
            '* 12,13 * * * * *',
            '1 1 1 1 1 1 1',
            '0 0,30 */1 * * * *']
    bad = ['* * * * * *',
           '1/12 * * * * * *',
           '* d * * * * *',
           '* * * * * * * *',
           '* + * * * * *',
           '0 q,30 */1 * * * *',
           '0 0,gasd */1 * * * *',
           '0 0,30 */rt * * * *',
           '0 0,,,9 */1 * * * *']
    for rule in good:
        try:
            validate_rule(rule)
        except ValueError:
            assert False, f'Exception with rule "{rule}"'
    for rule in bad:
        try:
            validate_rule(rule)
        except ValueError:
            pass
        else:
            assert False, f'Wrong rule passed "{rule}"'
    assert True
