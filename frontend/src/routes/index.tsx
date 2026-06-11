import { createFileRoute, Link } from "@tanstack/react-router";
import { Plane, CloudSun, BarChart3, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import heroJet from "@/assets/hero-jet.jpg";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "AeroPredict — Know Your Flight Delay Before You Fly" },
      {
        name: "description",
        content:
          "AeroPredict forecasts your flight delay using airline, schedule, distance and weather data. Travel smarter with delay predictions in seconds.",
      },
      { property: "og:title", content: "AeroPredict — Know Your Flight Delay Before You Fly" },
      {
        property: "og:description",
        content: "Forecast flight delays from airline, schedule, distance and weather details.",
      },
    ],
  }),
  component: Index,
});

const features = [
  {
    icon: BarChart3,
    title: "Data-Driven Forecasts",
    text: "Predictions built on patterns across millions of historical flights — airline performance, routes and seasonality all factored in.",
  },
  {
    icon: CloudSun,
    title: "Weather Aware",
    text: "Weather is the single biggest cause of delays. AeroPredict folds reported weather delay into every estimate it makes.",
  },
  {
    icon: Clock,
    title: "Answers in Seconds",
    text: "Enter six simple details about your flight and get an instant delay estimate — no account, no waiting, no surprises at the gate.",
  },
];

const stats = [
  { value: "6", label: "Flight details analyzed" },
  { value: "12", label: "Months of seasonality" },
  { value: "24/7", label: "Instant predictions" },
];

function Index() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <header className="absolute top-0 z-20 w-full">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
          <Link to="/" className="flex items-center gap-2">
            <Plane className="h-5 w-5 text-primary" />
            <span className="font-display text-xl tracking-luxe text-foreground">AEROPREDICT</span>
          </Link>
          <Button variant="heroOutline" size="sm" asChild>
            <Link to="/predict">Get Started</Link>
          </Button>
        </nav>
      </header>

      {/* Hero */}
      <section className="relative flex min-h-screen items-center justify-center overflow-hidden">
        <img
          src={heroJet}
          alt="Jet airliner flying through dark clouds at dusk"
          width={1920}
          height={1080}
          className="absolute inset-0 h-full w-full object-cover"
        />
        <div className="hero-overlay absolute inset-0" />
        <div className="relative z-10 mx-auto max-w-3xl px-6 text-center">
          <h1 className="font-display text-5xl leading-tight text-foreground md:text-7xl">
            Aero<span className="text-gradient-gold">Predict</span>
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-base font-light leading-relaxed text-muted-foreground md:text-lg">
            Know whether your flight will leave on time — before you even pack. AeroPredict
            estimates your delay from your airline, schedule, route distance and the weather, so
            you can plan every journey with confidence.
          </p>
          <div className="mt-10">
            <Button variant="hero" size="xl" asChild>
              <Link to="/predict">Get Started</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* About */}
      <section className="mx-auto max-w-6xl px-6 py-24">
        <div className="mb-16 text-center">
          <p className="mb-3 text-xs uppercase tracking-luxe text-primary">Why AeroPredict</p>
          <h2 className="font-display text-3xl text-foreground md:text-4xl">
            Travel With Certainty
          </h2>
        </div>
        <div className="grid gap-8 md:grid-cols-3">
          {features.map((f) => (
            <article
              key={f.title}
              className="shadow-card-deep border border-border bg-card p-8 transition-colors duration-300 hover:border-primary/40"
            >
              <f.icon className="mb-5 h-7 w-7 text-primary" />
              <h3 className="mb-3 font-display text-lg tracking-wide text-foreground">{f.title}</h3>
              <p className="text-sm font-light leading-relaxed text-muted-foreground">{f.text}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Stats band */}
      <section className="border-y border-border bg-card/50">
        <div className="mx-auto grid max-w-5xl gap-10 px-6 py-16 text-center sm:grid-cols-3">
          {stats.map((s) => (
            <div key={s.label} className="border border-primary/30 px-6 py-10">
              <div className="font-display text-4xl text-primary">{s.value}</div>
              <div className="mt-2 text-xs uppercase tracking-luxe text-muted-foreground">
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-3xl px-6 py-24 text-center">
        <h2 className="font-display text-3xl leading-snug text-foreground md:text-4xl">
          Check your flight
          <br />
          <span className="text-gradient-gold">and arrive prepared.</span>
        </h2>
        <p className="mx-auto mt-5 max-w-md text-sm font-light leading-relaxed text-muted-foreground">
          Six details. One click. A clear picture of what to expect at departure.
        </p>
        <div className="mt-8">
          <Button variant="hero" size="xl" asChild>
            <Link to="/predict">Get Started</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-8 sm:flex-row">
          <div className="flex items-center gap-2">
            <Plane className="h-4 w-4 text-primary" />
            <span className="font-display text-sm tracking-luxe text-foreground">AEROPREDICT</span>
          </div>
          <p className="text-xs text-muted-foreground">
            © 2026 AeroPredict. Fly informed.
          </p>
        </div>
      </footer>
    </div>
  );
}
