import { useState } from "react";
import RecipeCard from "../ui/cards/recipe-card";
import ProposalCard from "../chat/ProposalCard";
import Button from "../ui/Button";
import { RotateCw, Loader2 } from "lucide-react";

type Meal = {
  title: string;
  calories: number;
  description: string;
  image?: string;
};

export default function MealItem({ meal }: { meal: Meal }) {
  const [proposal, setProposal] = useState<Meal | null>(null);
  const [loading, setLoading] = useState(false);

  const handleRequestChange = async () => {
    setLoading(true);
    try {
      // Simulación de llamada a la API
      // const res = await fetch('/api/change-meal', { method: 'POST', body: JSON.stringify(meal) });
      // const newData = await res.json();
      
      // Simulación de delay y datos de vuelta
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockNewMeal = {
        title: "Nueva Receta Sugerida",
        calories: 450,
        description: "Una alternativa saludable basada en tus gustos.",
        image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
      };

      setProposal(mockNewMeal);
    } catch (error) {
      console.error("Error al cambiar la receta", error);
    } finally {
      setLoading(false);
    }
  };

  // Si hay una propuesta, mostramos la ProposalCard
  if (proposal) {
    return (
      <ProposalCard
        image={proposal.image || ""}
        badge="Sugerencia Nueva"
        title={proposal.title}
        description={proposal.description}
        onConfirm={() => {
          // Aquí lógica para guardar en DB
          console.log("Confirmado");
          // Podrías actualizar el estado global o simplemente limpiar la propuesta si ya se guardó
        }}
        onCancel={() => setProposal(null)} // Volver a la original
      />
    );
  }

  // Si no hay propuesta, mostramos la RecipeCard original
  return (
    <RecipeCard {...meal} image={meal.image || ""}>
      <Button 
        variant="primary" 
        onClick={handleRequestChange}
        disabled={loading}
        className="w-full flex items-center justify-center gap-2"
      >
        {loading ? (
          <Loader2 className="size-4 animate-spin" />
        ) : (
          <RotateCw className="size-4" />
        )}
        <span>{loading ? "Buscando..." : "Cambiar"}</span>
      </Button>
    </RecipeCard>
  );
}