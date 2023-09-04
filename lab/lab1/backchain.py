from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    results = [hypothesis]
    for rule in rules:
        expr = rule.consequent()[0]
        bindings = match(expr, hypothesis)
        if bindings or expr == hypothesis:          # there is no variables in hypothesis in TEST 14(data in tests.py)
            antecedent = rule.antecedent()
            if isinstance(antecedent, AND):
                new_results = []
                for item in populate(rule.antecedent(), bindings):
                    new_results.append(backchain_to_goal_tree(rules, item))
                results.append(AND(new_results))
            elif isinstance(antecedent, OR):
                new_results = []
                for item in populate(rule.antecedent(), bindings):
                    new_results.append(backchain_to_goal_tree(rules, item))
                results.append(OR(new_results))
            else:
                new_hypothesis = populate(antecedent, bindings)
                results.append(backchain_to_goal_tree(rules, new_hypothesis))
                results.append(new_hypothesis)
    return simplify(OR(results))



# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
