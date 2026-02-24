import { useState, KeyboardEvent } from "react";


type Props = {
  meals: number;
  setMeals: (n: number) => void;
  dietTypes: string[];
  setDietTypes: (diets: string[]) => void;
};


export default function PreferencesSection({ meals, setMeals, dietTypes, setDietTypes }: Props) {
  const [allergies, setAllergies] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState("");
  const addAllergy = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && inputValue.trim()) {
      e.preventDefault();
      setAllergies([...allergies, inputValue.trim()]);
      setInputValue("");
    }
  };

  const removeAllergy = (allergy: string) => {
    setAllergies(allergies.filter((a) => a !== allergy));
  };

  const options = [3, 4, 5, 6];
  // Enums backend: high_protein, low_carb, vegan, vegetarian, low_calorie, high_fiber, high_carb
  const dietOptions = [
    { value: "high_protein", label: "High Protein" },
    { value: "low_carb", label: "Low Carb" },
    { value: "vegan", label: "Vegan" },
    { value: "vegetarian", label: "Vegetarian" },
    { value: "low_calorie", label: "Low Calorie" },
    { value: "high_fiber", label: "High Fiber" },
    { value: "high_carb", label: "High Carb" },
  ];

  const toggleDiet = (diet: string) => {
    setDietTypes(
      dietTypes.includes(diet)
        ? dietTypes.filter((d) => d !== diet)
        : [...dietTypes, diet]
    );
  };

  return (
    <section className="bg-gradient-to-br from-green-950/70 to-green-900/50 rounded-xl p-6 flex flex-col gap-6 h-full flex-1">
      <h2 className="text-xl font-bold mb-4">Preferences</h2>

      {/* Comidas por día */}
      <div>
        <p className="text-text-secondary text-sm mb-3 font-medium">Meals per day</p>
        <div className="flex flex-wrap gap-2">
          {options.map((n) => (
            <button
              key={n}
              onClick={() => setMeals(n)}
              className={`flex-1 min-w-[48px] py-2 rounded-md text-sm transition hover:bg-primary/10 hover:text-primary hover:border-primary border ${
                meals === n
                  ? "bg-primary text-black font-bold border-primary"
                  : "bg-surface-dark text-text-secondary border-surface-border"
              }`}
            >
              {n === 6 ? "6" : n}
            </button>
          ))}
        </div>
      </div>

      {/* Diet Type */}
      <div className="flex flex-col gap-2">
        <span className="text-text-secondary text-sm mb-2 font-medium">
          Diet Types
        </span>
        <div className="flex flex-wrap gap-y-3 gap-x-2">
          {dietOptions.map((diet) => (
            <label key={diet.value} className="cursor-pointer flex-shrink-0">
              <input
                type="checkbox"
                className="absolute opacity-0 w-0 h-0 pointer-events-none peer"
                checked={dietTypes.includes(diet.value)}
                onChange={() => toggleDiet(diet.value)}
              />
              <span className="px-3 py-1.5 rounded-full border border-surface-border bg-surface-dark text-text-secondary text-sm peer-checked:border-primary peer-checked:text-primary peer-checked:bg-primary/10 transition-colors whitespace-nowrap hover:border-primary hover:text-primary hover:bg-primary/10">
                {diet.label}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Allergies and intolerances */}
      <div className="flex flex-col gap-2">
        <span className="text-text-secondary text-sm font-medium">
          Allergies and Intolerances
        </span>
        <div className="bg-surface-dark border border-surface-border rounded-lg p-2 flex flex-wrap gap-2 items-center focus-within:ring-1 focus-within:ring-primary focus-within:border-primary transition-all min-h-[48px]">
          {allergies.map((allergy) => (
            <span
              key={allergy}
              className="flex items-center gap-1 bg-[#2d4036] text-white text-xs px-2 py-1 rounded"
            >
              <span className="flex items-center h-full">{allergy}</span>
              <button
                type="button"
                onClick={() => removeAllergy(allergy)}
                className="flex items-center justify-center hover:text-red-400 h-5"
                style={{ lineHeight: 0 }}
              >
                <span className="inline-flex items-center justify-center w-4 h-4 align-middle">
                  <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-4 h-4">
                    <rect x="1" y="1" width="14" height="14" rx="3" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="1.2" />
                    <path d="M5.5 5.5L10.5 10.5M10.5 5.5L5.5 10.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
                  </svg>
                </span>
              </button>
            </span>
          ))}
          <input
            type="text"
            className="bg-transparent border-none outline-none ring-0 focus:ring-0 focus:outline-none text-white text-sm placeholder:text-surface-border min-w-[100px] p-1 flex-grow"
            placeholder="Add..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={addAllergy}
          />
        </div>
        <p className="text-xs text-text-secondary">
          Type and press enter to add.
        </p>
      </div>
    </section>
  );
}
