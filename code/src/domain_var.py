# GOAL CONTROL
goal_control_emotions = ["joyful", "frustrated", "grateful", "disappointed"]
goal_control_template = """Context: {context}
Action: {action}
Outcome Goal 1: {outcome_goal1}
Outcome Goal 2: {outcome_goal2}
Goal Belief 1: {goal1}
Goal Belief 2: {goal2}
Control Belief: {control}
Lack of Control Belief: {uncontrol}
Outcome question: {outcome_question} 
Outcome answer 1: {outcome_answer1}
Outcome answer 2: {outcome_answer2}
Belief question a: {belief_question_a}
Belief answer 1a: {belief_answer_1a}
Belief answer 2a: {belief_answer_2a}
Belief question b: {belief_question_b}
Belief answer 1b: {belief_answer_1b}
Belief answer 2b: {belief_answer_2b}
"""
goal_control_template_var = ["context", "action",   "outcome_goal1", "outcome_goal2", "goal1", "goal2", "control", "uncontrol",
                            "outcome_question", "outcome_answer1", "outcome_answer2", "belief_question_a", "belief_answer_1a",
                            "belief_answer_2a", "belief_question_b", "belief_answer_1b", "belief_answer_2b"]
goal_control_list_var = ["Context", "Action",  "Outcome Goal 1", "Outcome Goal 2", "Goal Belief 1", "Goal Belief 2", "Control Belief", "Lack of Control Belief", 
    "Outcome question", "Outcome answer 1", "Outcome answer 2", "Belief question a", "Belief answer 1a", "Belief answer 2a", "Belief question b", "Belief answer 1b", "Belief answer 2b"]

# SAFETY EXPECTED
safety_expected_emotions = ["relieved", "resigned", "surprised", "devastated"]
safety_expected_template = """Context: {context}
Action: {action}
Outcome 1: {outcome1}
Outcome 2: {outcome2}
Safety Belief 1: {safety_belief1}
Safety Belief 2: {safety_belief2}
Expectedness: {expectedness}
Unexpectedness: {unexpectedness}
Outcome question: {outcome_question} 
Outcome answer 1: {outcome_answer1}
Outcome answer 2: {outcome_answer2}
Belief question a: {belief_question_a}
Belief answer 1a: {belief_answer_1a}
Belief answer 2a: {belief_answer_2a}
Belief question b: {belief_question_b}
Belief answer 1b: {belief_answer_1b}
Belief answer 2b: {belief_answer_2b}
"""
safety_expected_template_var = ["context", "action", "outcome1", "outcome2", "safety_belief1", "safety_belief2", "expectedness", "unexpectedness",
                                "outcome_question", "outcome_answer1", "outcome_answer2", "belief_question_a", "belief_answer_1a",
                            "belief_answer_2a", "belief_question_b", "belief_answer_1b", "belief_answer_2b"]
safety_expected_list_var = ["Context", "Action", "Outcome 1", "Outcome 2", "Safety Belief 1", "Safety Belief 2", "Expectedness", "Unexpectedness",
                            "Outcome question", "Outcome answer 1", "Outcome answer 2", "Belief question a", "Belief answer 1a", "Belief answer 2a",
                            "Belief question b", "Belief answer 1b", "Belief answer 2b"]
