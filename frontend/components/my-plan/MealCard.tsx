type Meal = {
  title: string;
  kcal: number;
  description: string;
};

export default function MealCard({ meal }: { meal: Meal }) {
  return (
    <div className="bg-surface-dark border border-[#283930] rounded-xl p-4 flex flex-col gap-2">
      <div className="flex justify-between">
        <h4 className="font-bold">{meal.title}</h4>
        <span className="text-primary text-sm font-bold">
          {meal.kcal} kcal
        </span>
      </div>
      <p className="text-sm text-[#9db9ab]">
        {meal.description}
      </p>
      <button className="mt-auto bg-[#283930] py-2 rounded-lg text-sm">
        Cambiar
      </button>
    </div>
  );
}
