import { useState } from "react";
import RecipeCard from "../ui/cards/recipe-card";
import ProposalCard from "../chat/ProposalCard";
import Button from "../ui/Button";
import { RotateCw, Loader2 } from "lucide-react";

type Meal = {
  id?: number;
  recipeId?: number;
  title: string;
  calories: number;
  description: string;
  images?: string[];
};

export default function MealItem({ meal }: { meal: Meal }) {
  const [currentMeal, setCurrentMeal] = useState<Meal>(meal);
  const [proposal, setProposal] = useState<Meal | null>(null);
  const [loading, setLoading] = useState(false);
  const [confirming, setConfirming] = useState(false);

  const handleRequestChange = async () => {
    setLoading(true);
    try {
      // TODO: reemplazar con llamada real a la API para obtener sugerencia
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockNewMeal: Meal = {
        recipeId: 2, // ID de la receta propuesta (viene de la API en producción)
        title: "New Suggested Recipe",
        calories: 450,
        description: "A healthy alternative based on your preferences.",
        images: ["https://images.unsplash.com/photo-1546069901-ba9599a7e63c"],
      };
      setProposal(mockNewMeal);
      /* ############################################# 
          Cuando este integrado el modelo KNN, el flujo será:
        ############################################# */
        // Reemplazar el mock por:
        /* const res = await fetch(
          `http://localhost:8000/api/recipes/suggest?meal_detail_id=${currentMeal.id}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        const data = await res.json();
        setProposal({
          recipeId: data.id,
          title: data.name,
          calories: data.calories,
          description: data.meal_type ?? "",
          images: getAllImages(data.image_url),
        }); */
    } catch (error) {
      console.error("Error changing recipe", error);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    if (!proposal) return;
    setConfirming(true);
    try {
      // Llamada real al backend: PUT /api/meal-detail/{id}?recipe_id={recipeId}
      if (currentMeal.id && proposal.recipeId) {
        const token = localStorage.getItem("token");
        const res = await fetch(
          `http://localhost:8000/api/meal-detail/${currentMeal.id}?recipe_id=${proposal.recipeId}`,
          {
            method: "PUT",
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        if (!res.ok) throw new Error("Failed to update meal");
      }
      // Actualizar estado local: reemplazar la receta mostrada con la propuesta
      setCurrentMeal({ ...proposal, id: currentMeal.id });
      setProposal(null);
    } catch (error) {
      console.error("Error confirming meal change", error);
    } finally {
      setConfirming(false);
    }
  };

  // Si hay una propuesta, mostrar el ProposalCard
  if (proposal) {
    return (
      <ProposalCard
        image={proposal.images?.[0] || ""}
        badge="New Suggestion"
        title={proposal.title}
        description={proposal.description}
        onConfirm={handleConfirm}
        onCancel={() => setProposal(null)}
      />
    );
  }

  // Si no hay propuesta, mostrar la receta actual con opción a cambiar
  return (
    <RecipeCard {...currentMeal} images={currentMeal.images ?? []}>
      <Button 
        variant="primary" 
        onClick={handleRequestChange}
        disabled={loading || confirming}
        className="w-full flex items-center justify-center gap-2"
      >
        {loading ? (
          <Loader2 className="size-4 animate-spin" />
        ) : (
          <RotateCw className="size-4" />
        )}
        <span>{loading ? "Searching..." : "Change"}</span>
      </Button>
    </RecipeCard>
  );
}