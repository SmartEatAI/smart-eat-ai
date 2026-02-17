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
        title: "New Suggested Recipe",
        calories: 450,
        description: "A healthy alternative based on your preferences.",
        image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
      };

      setProposal(mockNewMeal);
    } catch (error) {
      console.error("Error changing recipe", error);
    } finally {
      setLoading(false);
    }
  };

  // If there is a proposal, show the ProposalCard
  if (proposal) {
    return (
      <ProposalCard
        image={proposal.image || ""}
        badge="New Suggestion"
        title={proposal.title}
        description={proposal.description}
        onConfirm={() => {
          // Logic to save in DB
          console.log("Confirmed");
          // You could update global state or simply clear the proposal if already saved
        }}
        onCancel={() => setProposal(null)} // Return to original
      />
    );
  }

  // If there is no proposal, show the original RecipeCard
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
        <span>{loading ? "Searching..." : "Change"}</span>
      </Button>
    </RecipeCard>
  );
}