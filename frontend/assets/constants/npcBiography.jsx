import { getNpcSummary } from "./npcLabels";

function getPronouns(sex) {
  if (sex === "F") {
    return {
      subject: "She",
      possessive: "her",
    };
  }

  return {
    subject: "He",
    possessive: "his",
  };
}

function getOccupationText(npc) {
  const age = Number(npc.age);
  const isUnemployed = !npc.occupation || npc.occupation === "Unemployed";

  if (isUnemployed) {
    if (age < 18) {
      return "is still growing up and not part of the workforce yet";
    }

    if (age >= 65) {
      return "is no longer part of the active workforce";
    }

    return "is currently between occupations";
  }

  return `works as ${npc.occupation}`;
}

function getCareerStatusText(npc, pronouns) {
  const age = Number(npc.age);
  const level = Number(npc.job_level);
  const isUnemployed = !npc.occupation || npc.occupation === "Unemployed";

  if (age < 18 || isUnemployed) return "";

  if (level >= 7) {
    return ` ${pronouns.subject} has reached an advanced stage in ${pronouns.possessive} career and lives a financially secure life.`;
  }

  if (level >= 4) {
    return ` ${pronouns.subject} lives a stable and comfortable life without major financial difficulties.`;
  }

  return ` ${pronouns.subject} belongs to the lower economic layer and sometimes struggles with daily expenses.`;
}

function describeLevel(value, descriptions, pronouns) {
  const number = Number(value);

  if (number >= 80) return descriptions.high(pronouns);
  if (number >= 50) return descriptions.medium(pronouns);
  return descriptions.low(pronouns);
}

const healthDescriptions = {
  high: (p) => `${p.subject} appears physically strong and healthy.`,
  medium: (p) => `${p.subject} seems to be in stable physical condition.`,
  low: (p) => `${p.subject} appears physically weakened.`,
};

const energyDescriptions = {
  high: (p) => `${p.subject} seems energetic and active.`,
  medium: (p) => `${p.subject} shows a moderate level of energy.`,
  low: (p) => `${p.subject} seems somewhat tired.`,
};

const stressDescriptions = {
  high: (p) => `${p.subject} appears visibly burdened by stress.`,
  medium: (p) =>
    `${p.subject} seems to manage daily pressures reasonably well.`,
  low: (p) => `${p.subject} appears calm and relaxed.`,
};

function getConditionText(npc) {
  if (!npc.degenerative_condition || npc.degenerative_condition === "none") {
    return "";
  }

  return ` Some behavioral patterns suggest traits associated with ${npc.degenerative_condition}.`;
}

export function getNpcBiography(npc) {
  if (!npc) return "";

  const pronouns = getPronouns(npc.sex);

  const fullName = `${npc.first_name} ${npc.last_name}`;
  const sex = npc.sex === "F" ? "female" : "male";

  const occupationSentence = getOccupationText(npc);
  const careerSentence = getCareerStatusText(npc, pronouns);

  const healthSentence = describeLevel(
    npc.health_level,
    healthDescriptions,
    pronouns,
  );

  const energySentence = describeLevel(
    npc.energy_level,
    energyDescriptions,
    pronouns,
  );

  const stressSentence = describeLevel(
    npc.stress_level,
    stressDescriptions,
    pronouns,
  );

  const conditionSentence = getConditionText(npc);

  return `${fullName} is a ${npc.age}-year-old ${sex} who ${occupationSentence}.${careerSentence}

${getNpcSummary(npc)}

${healthSentence} ${energySentence} ${stressSentence}${conditionSentence}`;
}
