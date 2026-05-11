from typing import Dict  # import Dict type for type hints


PERSONALITY_TYPES = ["analytical", "creative", "social",
                     "leadership"]  # a list of personality types


def init_scores() -> Dict[str, int]:
    # create a dictionary with all personality types and set to 0 for first value
    return {ptype: 0 for ptype in PERSONALITY_TYPES}


def calculate_personality(scores: Dict[str, int]) -> str:
    # return the personality type with the highest score and then personality will be determined
    return max(scores, key=scores.get)


def personality_to_skills(personality_dict: Dict[str, int]) -> Dict[str, int]:
    # calculate total score of all personality types
    total = sum(personality_dict.values())

    # if total is 0, return all skills as 0
    if total == 0:
        return {k: 0 for k in personality_dict}

    # convert personality scores into skill scores (scale to 0-10)
    return {
        # analytical skill
        "analytical": round(personality_dict["analytical"] / total * 10, 2),
        # logic based on analytical
        "logic": round(personality_dict["analytical"] / total * 10, 2),
        # creativity skill
        "creativity": round(personality_dict["creative"] / total * 10, 2),
        # communication skill
        "communication": round(personality_dict["social"] / total * 10, 2),
        # leadership skill
        "leadership": round(personality_dict["leadership"] / total * 10, 2)
    }


def merge_skills(personality_skills, user_skills):

    final = {}  # dictionary to store final merged skills

    # loop through each skill from personality skills
    for skill in personality_skills:
        # get personality skill value
        personality_value = personality_skills[skill]
        # get user skill value (default 0)
        user_value = user_skills.get(skill, 0)

        avg = (personality_value + user_value) / 2  # calculate average of both

        final[skill] = round(avg, 2)  # round to 2 decimals

    return final  # return final merged skills
