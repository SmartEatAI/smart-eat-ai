"use client";

import Image from "next/image";
import Button from "@/components/ui/Button";
import Section from "@/components/layout/section";
import { Card, CardContent } from "@/components/ui/card";
import { Clock, Heart, Leaf } from "lucide-react";
import Step from "@/components/ui/step";
import PlanCard from "@/components/ui/cards/plan-card";
import ReviewCard from "@/components/ui/cards/review-card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import Autoplay from "embla-carousel-autoplay";
import { useRef } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { Review } from "@/types/landing";
import PublicRoute from '../components/auth/PublicRoute';

const reviews: Review[] = [
  {
    name: "Emily Carter",
    image:
      "https://r-charts.com/es/miscelanea/procesamiento-imagenes-magick_files/figure-html/importar-imagen-r.png",
    rating: 5,
    review:
      "SmartEatAI completely changed how I plan my meals. I save so much time and I eat healthier without thinking about it.",
  },
  {
    name: "Daniel Moore",
    image:
      "https://r-charts.com/es/miscelanea/procesamiento-imagenes-magick_files/figure-html/importar-imagen-r.png",
    rating: 5,
    review:
      "The AI suggestions are surprisingly accurate. The grocery lists alone are worth it.",
  },
  {
    name: "Sophia Lee",
    image:
      "https://r-charts.com/es/miscelanea/procesamiento-imagenes-magick_files/figure-html/importar-imagen-r.png",
    rating: 4,
    review:
      "I love how easy it is to follow. Less food waste, better meals, and zero stress.",
  },
  {
    name: "Michael Brown",
    image:
      "https://r-charts.com/es/miscelanea/procesamiento-imagenes-magick_files/figure-html/importar-imagen-r.png",
    rating: 5,
    review:
      "Meal planning has never been this simple. The personalization is spot on.",
  },
];

export default function Home() {
  const autoplay = useRef(Autoplay({ delay: 8000, stopOnInteraction: true }));

  return (
    <PublicRoute>
      <main className="w-full min-h-screen">
        <Navbar />
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
            <div className="relative w-full h-75 md:h-100 overflow-hidden rounded-xl group">
              <Image
                src="https://marmitafitnesssp.com.br/wp-content/uploads/2023/04/Refeicoes-Fitness-Sao-Paulo.jpg"
                alt="Healthy food"
                fill
                className="object-cover rounded-xl transition-all duration-500 ease-in-out group-hover:scale-110 group-hover:brightness-75"
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

        {/* SECCIÓN DE PRICING */}
        <Section
          id="plans"
          title="Simple & Transparent Plans"
          subtitle="Choose a plan that fits your lifestyle and start eating smarter today."
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* BASIC */}
            <PlanCard
              title="Basic"
              price="Free"
              description="Perfect to get started"
              features={[
                "Basic meal recommendations",
                "Limited recipes access",
                "Standard grocery list",
              ]}
              buttonText="Get started"
            />

            {/* PRO */}
            <PlanCard
              title="Pro"
              price="$9 / month"
              description="Most popular choice"
              features={[
                "Personalized AI meal plans",
                "Unlimited recipes",
                "Smart grocery lists",
                "Nutrition insights",
              ]}
              highlighted
              buttonText="Start free trial"
            />

            {/* PREMIUM */}
            <PlanCard
              title="Premium"
              price="$19 / month"
              description="For maximum control & results"
              features={[
                "Everything in Pro",
                "Advanced nutrition analytics",
                "Custom dietary goals",
                "Priority support",
              ]}
              buttonText="Go premium"
            />
          </div>
        </Section>

        {/* SECCIÓN DE TESTIMONIOS */}
        <Section
          id="reviews"
          title="What Our Users Say"
          subtitle="Real experiences from people using SmartEatAI every day."
        >
          <div className="relative">
            <Carousel plugins={[autoplay.current]} opts={{ loop: true }}>
              <CarouselContent>
                {reviews.map((review, index) => (
                  <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">
                    <ReviewCard {...review} />
                  </CarouselItem>
                ))}
              </CarouselContent>

              <CarouselPrevious className="hidden lg:flex -left-4 xl:-left-12" />

              <CarouselNext className="hidden lg:flex -right-4 xl:-right-12" />
            </Carousel>
          </div>
        </Section>

        {/* SECCIÓN DE LLAMADO A LA ACCIÓN FINAL */}
        <Section id="cta" className="mt-12">
          <div className="rounded-2xl bg-primary text-primary-foreground px-6 py-16 text-center flex flex-col items-center gap-6">

            <p className="text-2xl md:text-3xl font-bold max-w-2xl">
              Start eating smarter today.
            </p>

            <p className="text-sm md:text-base opacity-90 max-w-xl">
              Create your personalized meal plan in minutes and take control of
              your nutrition with SmartEatAI.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button variant="primary">
                <Link href="/auth">
                  Get started for free
                </Link>
              </Button>
            </div>

          </div>
        </Section>
        <Footer />
      </main>
    </PublicRoute>
  );
}
