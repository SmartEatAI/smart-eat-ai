import { useState, KeyboardEvent } from "react";
import { Category } from "@/types/category";

type Props = {
  meals: number;
  setMeals: (n: number) => void;
  dietTypes: (string | Category)[];
  setDietTypes: (diets: string[]) => void;
  restrictions: (string | Category)[];
  setRestrictions: (r: string[]) => void;
  tastes: (string | Category)[];
  setTastes: (t: string[]) => void;
};


export default function PreferencesSection({ 
  meals, setMeals, dietTypes, setDietTypes,
  restrictions, setRestrictions, tastes, setTastes
}: Props) {

  
  {/* Restrictions and tastes */}
  const [restrictionInput, setRestrictionInput] = useState("");
  const [tasteInput, setTasteInput] = useState("");

  // Extraer el nombre sin importar el formato de entrada
  const getNames = (arr: (string | Category)[]): string[] => {
    if (!Array.isArray(arr)) return [];
    return arr.map(item => typeof item === 'string' ? item : item.name);
  };

  const dietNames = getNames(dietTypes);

  const handleAddTag = (
    e: KeyboardEvent<HTMLInputElement>, 
    currentItems: (string | Category)[], 
    setter: (val: string[]) => void, 
    inputSetter: (val: string) => void,
    inputValue: string
  ) => {
    if (e.key === "Enter" && inputValue.trim()) {
      e.preventDefault();
      const currentNames = getNames(currentItems);
      if (!currentNames.includes(inputValue.trim())) {
        setter([...currentNames, inputValue.trim()]);
      }
      inputSetter("");
    }
  };

  const handleRemoveTag = (name: string, currentItems: (string | Category)[], setter: (val: string[]) => void) => {
    setter(getNames(currentItems).filter((n) => n !== name));
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

  const toggleDiet = (dietValue: string) => {
    const nextDiets = dietNames.includes(dietValue)
      ? dietNames.filter((d) => d !== dietValue)
      : [...dietNames, dietValue];
    setDietTypes(nextDiets);
  };


return (
    <section className="bg-gradient-to-br from-green-950/70 to-green-900/50 rounded-xl p-6 flex flex-col gap-6 h-full flex-1">
      {/* Meals per day */}
      <div>
        <p className="text-text-secundary text-sm mb-3 font-medium">Meals per day</p>
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
              {n}
            </button>
          ))}
        </div>
      </div>

      {/* Diet Types - Ahora usa dietNames para verificar el estado */}
      <div className="flex flex-col gap-2">
        <span className="text-text-secondary text-sm mb-2 font-medium">Diet Types</span>
        <div className="flex flex-wrap gap-y-3 gap-x-2">
          {dietOptions.map((diet) => (
            <label key={diet.value} className="cursor-pointer">
              <input
                type="checkbox"
                className="hidden peer"
                checked={dietNames.includes(diet.value)}
                onChange={() => toggleDiet(diet.value)}
              />
              <span className="px-3 py-1.5 rounded-full border border-surface-border bg-surface-dark text-text-secondary text-sm peer-checked:border-primary peer-checked:text-primary peer-checked:bg-primary/10 transition-colors whitespace-nowrap hover:border-primary hover:text-primary hover:bg-primary/10">
                {diet.label}
              </span>
            </label>
          ))}
        </div>
      </div>

      <TagInputGroup 
        label="Restrictions"
        placeholder="Add allergy..."
        items={getNames(restrictions)}
        inputValue={restrictionInput}
        setInputValue={setRestrictionInput}
        onKeyDown={(e) => handleAddTag(e, restrictions, setRestrictions, setRestrictionInput, restrictionInput)}
        onRemove={(name) => handleRemoveTag(name, restrictions, setRestrictions)}
      />

      <TagInputGroup 
        label="Tastes"
        placeholder="Add preference..."
        items={getNames(tastes)}
        inputValue={tasteInput}
        setInputValue={setTasteInput}
        onKeyDown={(e) => handleAddTag(e, tastes, setTastes, setTasteInput, tasteInput)}
        onRemove={(name) => handleRemoveTag(name, tastes, setTastes)}
      />
    </section>
  );
}

// Interfaz y componente TagInputGroup (igual que antes)
interface TagInputGroupProps {
  label: string;
  placeholder: string;
  items: string[];
  inputValue: string;
  setInputValue: (v: string) => void;
  onKeyDown: (e: KeyboardEvent<HTMLInputElement>) => void;
  onRemove: (name: string) => void;
}

function TagInputGroup({ label, placeholder, items, inputValue, setInputValue, onKeyDown, onRemove }: TagInputGroupProps) {
  return (
    <div className="flex flex-col gap-2">
      <p className="text-text-secundary text-sm mb-3 font-medium">{label}</p>
      <div className="bg-secondary/50 border border-border rounded-lg p-2 flex flex-wrap gap-2 items-center min-h-[48px] focus-within:ring-1 focus-within:ring-primary">
        {items.map((name, index) => (
          <span key={`${name}-${index}`} className="flex items-center gap-1 bg-primary/10 text-primary text-xs px-2 py-1 rounded-md border border-primary/20">
            {name}
            <button type="button" onClick={() => onRemove(name)} className="hover:text-destructive ml-1">×</button>
          </span>
        ))}
        <input
          type="text"
          className="bg-transparent border-none outline-none text-sm flex-grow min-w-[120px] p-1"
          placeholder={items.length === 0 ? placeholder : ""}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={onKeyDown}
        />
      </div>
    </div>
  );
}