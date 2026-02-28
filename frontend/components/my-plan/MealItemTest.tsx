import { useState } from "react";
import RecipeCard from "@/components/ui/cards/recipe-card";
import ProposalCard from "../chat/ProposalCard";
import Button from "../ui/Button";
import { RotateCw, Loader2 } from "lucide-react";
import { MealDetailResponse, RecipeResponse } from "@/types/my-plan";

interface Props {
  meal: MealDetailResponse;
  mealDetailId: number;
  swappable: boolean;
  onConfirmSwap: (mealDetailId: number, newRecipe: RecipeResponse) => Promise<void>;
  fetchNewRecipe: (mealType: string, recipeId: number) => Promise<RecipeResponse | null>;
}

export default function MealItemTest({
  meal,
  mealDetailId,
  swappable,
  onConfirmSwap,
  fetchNewRecipe,
}: Props) {
  const [loading, setLoading] = useState(false);
  const [proposal, setProposal] = useState<RecipeResponse | null>(null);

  const handleSwapClick = async () => {
    try {
      setLoading(true);

      const mealType = meal.meal_type;
      const newRecipe = await fetchNewRecipe(mealType, meal.recipe.recipe_id);

      if (newRecipe) {
        setProposal(newRecipe);
      }

    } catch (error) {
      console.error("Swap error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    if (!proposal) return;

    await onConfirmSwap(mealDetailId, proposal);
    setProposal(null);
  };

  const handleCancel = () => {
    setProposal(null);
  };

  const handleAnother = async () => {
    if (!meal.recipe) return;
    const newRecipe = await fetchNewRecipe(meal.meal_type, meal.recipe.recipe_id);
    if (newRecipe) setProposal(newRecipe);
  };

  if (proposal) {
    return (
      <ProposalCard
        image={proposal.image_url ?? ""}
        badge="New suggestion"
        title={proposal.name}
        confirmText="Accept"
        cancelText="Keep current"
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        extraInfo={
          <Button onClick={handleAnother} className="mt-2 w-full">
            Another suggestion
          </Button>
        }
      />
    );
  }

  return (
    <RecipeCard
      {...meal.recipe}
      title={meal.recipe.name}
      images={meal.recipe.image_url ?? ""}
      mealType={meal.recipe.meal_types}
      fats={meal.recipe.fat}
      recipeUrl={meal.recipe.recipe_url ?? ""}
    >
      {swappable && (
        <Button
          variant="primary"
          onClick={handleSwapClick}
          disabled={loading}
          className="w-full flex items-center justify-center gap-2"
        >
          {loading ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <RotateCw className="size-4" />
          )}
          <span>{loading ? "Searching..." : "Change"}</span>
        </Button>
      )}
    </RecipeCard>
  );
}