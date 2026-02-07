import Image from "next/image";
import { Button } from "@/components/ui/button";
import Section from "@/components/layout/section";
import { Card, CardContent } from "@/components/ui/cards/card";
import { Clock, Heart, Leaf } from "lucide-react";
import Step from "@/components/ui/step";

export default function Home() {
  return (
    <main className="w-full min-h-screen">
      {/* SECCIÓN DE INICIO */}
      <Section id="inicio">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center w-full">
          {/* LADO IZQUIERDO */}
          <div className="flex flex-col gap-6">
            <h1 className="text-4xl md:text-5xl font-bold leading-tight text-secondary">
              Welcome to <br />
              <span className="text-primary">SmartEat AI</span>
            </h1>

            <p className="text-muted-foreground max-w-md">
              SmartEat AI helps you plan healthier meals effortlessly using
              artificial intelligence tailored to your lifestyle.
            </p>

            <div className="flex gap-3 max-w-md">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 rounded-md border border-input bg-background px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
              <Button>Get early access</Button>
            </div>
          </div>

          {/* LADO DERECHO */}
          <div className="relative w-full h-[300px] md:h-[400px]">
            <Image
              src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
              alt="Healthy food"
              fill
              className="object-cover rounded-xl"
              priority
            />
          </div>
        </div>
      </Section>

      {/* SECCIÓN DE POR QUÉ ELEGIR SMART EAT AI */}
      <Section
        id="why-smarteat"
        title="Why choosing SmartEatAI"
        subtitle="Designed to make healthy eating simple, fast, and sustainable."
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="flex flex-col items-center text-center gap-4 p-6">
              <Clock className="h-10 w-10 text-primary" />
              <h3 className="text-lg font-semibold">Save Time</h3>
              <p className="text-sm text-muted-foreground">
                Get personalized meal plans in seconds and stop wasting time
                deciding what to eat every day.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex flex-col items-center text-center gap-4 p-6">
              <Heart className="h-10 w-10 text-primary" />
              <h3 className="text-lg font-semibold">Eat Healthier</h3>
              <p className="text-sm text-muted-foreground">
                Enjoy balanced meals tailored to your goals, preferences, and
                nutritional needs.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex flex-col items-center text-center gap-4 p-6">
              <Leaf className="h-10 w-10 text-primary" />
              <h3 className="text-lg font-semibold">Zero Food Waste</h3>
              <p className="text-sm text-muted-foreground">
                Plan smarter, use what you already have, and reduce food waste
                effortlessly.
              </p>
            </CardContent>
          </Card>
        </div>
      </Section>

      {/* SECCIÓN DE CÓMO FUNCIONA */}
      <Section
        id="how-it-works"
        title="How SmartEatAI Works"
        subtitle="From your preferences to ready-to-cook recipes in three simple steps."
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* LADO IZQUIERDO */}
          <div className="space-y-8">
            <Step
              number="1"
              title="Enter your details"
              description="Tell us about your goals, dietary preferences, allergies, and lifestyle so we can personalize your plan."
              variant="outline"
            />

            <Step
              number="2"
              title="AI creates your plan"
              description="Our artificial intelligence analyzes your data and generates a smart, balanced meal plan just for you."
              variant="muted"
            />

            <Step
              number="3"
              title="Get recipes & insights"
              description="Receive delicious recipes, shopping lists, and nutritional insights ready to use every day."
              variant="outline"
            />
          </div>

          {/* LADO DERECHO */}
          <div className="relative w-full aspect-video rounded-xl overflow-hidden border">
            <video
              className="w-full h-full object-cover"
              autoPlay
              muted
              loop
              playsInline
            >
              <source
                src="https://www.w3schools.com/html/mov_bbb.mp4"
                type="video/mp4"
              />
            </video>
          </div>
        </div>
      </Section>
    </main>
  );
}
