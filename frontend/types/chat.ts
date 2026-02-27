// Tipos
export type Recipe = {
    recipe_id: number;
    name: string;
    image_url: string;
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    meal_types: string[];
    diet_types: string[];
    recipe_url: string;
};

export type MessageBase = {
    role: "user" | "chef";
    text: string;
    time: Date;
};

export type MessageSuggestion = MessageBase & {
    sustitution: {
        original: Recipe;
        alternative: Recipe;
        accepted: boolean;
    };
};

export type MessageBubbleProps = {
    role: "user" | "chef";
    time: string;
    text: string;
    avatar: string;
};


export type Message = MessageBase | MessageSuggestion;
