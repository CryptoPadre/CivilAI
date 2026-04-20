export const fertilityLabels = {
  H: "High",
  N: "Normal",
  L: "Low",
};

export const happinessLines = {
  low: [
    "Looks weighed down by recent events.",
    "Seems tired and discouraged.",
    "Appears to be struggling today.",
  ],
  medium: [
    "Appears emotionally steady.",
    "Seems to be having an ordinary day.",
    "Looks balanced for the moment.",
  ],
  high: [
    "Seems genuinely content.",
    "Carries a cheerful presence.",
    "Looks satisfied with how things are going.",
  ],
};

export const aggressionLines = {
  low: ["Moves with a calm presence.", "Seems unlikely to seek conflict."],
  medium: [
    "Looks alert and guarded.",
    "Carries some tension beneath the surface.",
  ],
  high: ["Others may avoid provoking them.", "Seems ready for confrontation."],
};

export const empathyLines = {
  low: ["Keeps emotional distance from others.", "Appears socially detached."],
  medium: [
    "Shows a normal level of concern for others.",
    "Appears socially aware.",
  ],
  high: [
    "Seems highly sensitive to others’ feelings.",
    "Carries a warm presence.",
  ],
};

export const moralityLines = {
  low: [
    "Likely to follow self-interest first.",
    "May bend rules when convenient.",
  ],
  medium: [
    "Appears to follow common social boundaries.",
    "Seems reasonably principled.",
  ],
  high: [
    "Seems guided by strong personal principles.",
    "Carries a strong sense of integrity.",
  ],
};

function getLevel(value) {
  if (value <= 33) return "low";
  if (value <= 66) return "medium";
  return "high";
}

function randomFrom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

export function getNpcSummary(npc) {
  return [
    randomFrom(happinessLines[getLevel(npc.happiness_level)]),
    randomFrom(aggressionLines[getLevel(npc.aggression_level)]),
    randomFrom(empathyLines[getLevel(npc.empathy_level)]),
    randomFrom(moralityLines[getLevel(npc.morality_level)]),
  ].join(" ");
}
