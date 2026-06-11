import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { Plane, ArrowLeft, Timer } from "lucide-react";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const Route = createFileRoute("/predict")({
  head: () => ({
    meta: [
      { title: "Predict Your Flight Delay — AeroPredict" },
      {
        name: "description",
        content:
          "Enter your flight month, day, airline, departure time, distance and weather delay to get an instant delay prediction.",
      },
      { property: "og:title", content: "Predict Your Flight Delay — AeroPredict" },
      {
        property: "og:description",
        content: "Instant flight delay estimates from six simple details.",
      },
    ],
  }),
  component: PredictPage,
});

const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const AIRLINES = [
  { code: "AA", name: "American Airlines" },
  { code: "DL", name: "Delta Air Lines" },
  { code: "UA", name: "United Airlines" },
  { code: "WN", name: "Southwest Airlines" },
  { code: "B6", name: "JetBlue Airways" },
  { code: "AS", name: "Alaska Airlines" },
  { code: "NK", name: "Spirit Airlines" },
  { code: "F9", name: "Frontier Airlines" },
  { code: "HA", name: "Hawaiian Airlines" },
  { code: "G4", name: "Allegiant Air" },
];

const formSchema = z.object({
  month: z.string().nonempty("Select a month"),
  dayOfWeek: z.string().nonempty("Select a day of week"),
  airline: z.string().nonempty("Select an airline"),
  departureTime: z.string().nonempty("Enter a departure time"),
  distance: z
    .string()
    .nonempty("Enter the flight distance")
    .refine((v) => Number(v) > 0 && Number(v) <= 12000, "Distance must be between 1 and 12,000 miles"),
  weatherDelay: z
    .string()
    .nonempty("Enter the weather delay (0 if none)")
    .refine((v) => Number(v) >= 0 && Number(v) <= 1440, "Weather delay must be 0–1440 minutes"),
});

type FormValues = z.infer<typeof formSchema>;
type FormErrors = Partial<Record<keyof FormValues, string>>;

const toneClasses: Record<Prediction["tone"], string> = {
  success: "text-success border-success/40",
  warning: "text-warning border-warning/40",
  destructive: "text-destructive border-destructive/40",
};

function PredictPage() {
  const [values, setValues] = useState<FormValues>({
    month: "",
    dayOfWeek: "",
    airline: "",
    departureTime: "",
    distance: "",
    weatherDelay: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);

  const set = (key: keyof FormValues) => (value: string) => {
    setValues((v) => ({ ...v, [key]: value }));
    setErrors((e) => ({ ...e, [key]: undefined }));
    setPrediction(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const result = formSchema.safeParse(values);

    if (!result.success) {
      const next: FormErrors = {};

      for (const issue of result.error.issues) {
        const key = issue.path[0] as keyof FormValues;

        if (!next[key]) {
          next[key] = issue.message;
        }
      }

      setErrors(next);
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            Month: MONTHS.indexOf(values.month) + 1,
            DayOfWeek: DAYS.indexOf(values.dayOfWeek) + 1,
            Airline: values.airline,
            CRSDepTime: Number(values.departureTime.split(":")[0]),
            Distance: Number(values.distance),
            WeatherDelay: Number(values.weatherDelay),
          }),
        }
      );

      const data = await response.json();

      let label = "";
      let tone: "success" | "warning" | "destructive" =
        "success";

      if (data.prediction === 0) {
        label = "Green (On Time)";
        tone = "success";
      } else if (data.prediction === 1) {
        label = "Orange (Minor Delay)";
        tone = "warning";
      } else {
        label = "Red (Major Delay)";
        tone = "destructive";
      }

      setPrediction({
        minutes: data.delay_minutes,
        label,
        tone,
      });

    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <Link to="/" className="flex items-center gap-2">
            <Plane className="h-5 w-5 text-primary" />
            <span className="font-display text-xl tracking-luxe text-foreground">AEROPREDICT</span>
          </Link>
          <Link
            to="/"
            className="flex items-center gap-1.5 text-xs uppercase tracking-luxe text-muted-foreground transition-colors hover:text-primary"
          >
            <ArrowLeft className="h-3.5 w-3.5" />
            Home
          </Link>
        </nav>
      </header>

      <main className="mx-auto max-w-2xl px-6 py-16">
        <div className="mb-10 text-center">
          <p className="mb-3 text-xs uppercase tracking-luxe text-primary">Delay Forecast</p>
          <h1 className="font-display text-3xl text-foreground md:text-4xl">
            Your Flight Details
          </h1>
          <p className="mx-auto mt-4 max-w-md text-sm font-light leading-relaxed text-muted-foreground">
            Fill in the six details below and we'll estimate how late your flight is likely to be.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="shadow-card-deep border border-border bg-card p-8 md:p-10"
          noValidate
        >
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="space-y-2">
              <Label className="text-xs uppercase tracking-luxe text-muted-foreground">Month</Label>
              <Select value={values.month} onValueChange={set("month")}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select month" />
                </SelectTrigger>
                <SelectContent>
                  {MONTHS.map((m) => (
                    <SelectItem key={m} value={m}>{m}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.month && <p className="text-xs text-destructive">{errors.month}</p>}
            </div>

            <div className="space-y-2">
              <Label className="text-xs uppercase tracking-luxe text-muted-foreground">
                Day of Week
              </Label>
              <Select value={values.dayOfWeek} onValueChange={set("dayOfWeek")}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select day" />
                </SelectTrigger>
                <SelectContent>
                  {DAYS.map((d) => (
                    <SelectItem key={d} value={d}>{d}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.dayOfWeek && <p className="text-xs text-destructive">{errors.dayOfWeek}</p>}
            </div>

            <div className="space-y-2">
              <Label className="text-xs uppercase tracking-luxe text-muted-foreground">
                Airline Code
              </Label>
              <Select value={values.airline} onValueChange={set("airline")}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select airline" />
                </SelectTrigger>
                <SelectContent>
                  {AIRLINES.map((a) => (
                    <SelectItem key={a.code} value={a.code}>
                      {a.code} — {a.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.airline && <p className="text-xs text-destructive">{errors.airline}</p>}
            </div>

            <div className="space-y-2">
              <Label
                htmlFor="departureTime"
                className="text-xs uppercase tracking-luxe text-muted-foreground"
              >
                Departure Time
              </Label>
              <Input
                id="departureTime"
                type="time"
                value={values.departureTime}
                onChange={(e) => set("departureTime")(e.target.value)}
              />
              {errors.departureTime && (
                <p className="text-xs text-destructive">{errors.departureTime}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label
                htmlFor="distance"
                className="text-xs uppercase tracking-luxe text-muted-foreground"
              >
                Distance (miles)
              </Label>
              <Input
                id="distance"
                type="number"
                min={1}
                max={12000}
                placeholder="e.g. 950"
                value={values.distance}
                onChange={(e) => set("distance")(e.target.value)}
              />
              {errors.distance && <p className="text-xs text-destructive">{errors.distance}</p>}
            </div>

            <div className="space-y-2">
              <Label
                htmlFor="weatherDelay"
                className="text-xs uppercase tracking-luxe text-muted-foreground"
              >
                Weather Delay (min)
              </Label>
              <Input
                id="weatherDelay"
                type="number"
                min={0}
                max={1440}
                placeholder="e.g. 0"
                value={values.weatherDelay}
                onChange={(e) => set("weatherDelay")(e.target.value)}
              />
              {errors.weatherDelay && (
                <p className="text-xs text-destructive">{errors.weatherDelay}</p>
              )}
            </div>
          </div>

          <Button
            type="submit"
            variant="hero"
            size="xl"
            className="mt-10 w-full"
          >
            {loading ? "Predicting..." : "Predict Delay"}
          </Button>
        </form>

        {prediction && (
          <div
            className={`shadow-card-deep mt-8 border bg-card p-8 text-center ${toneClasses[prediction.tone]}`}
            role="status"
          >
            <Timer className="mx-auto mb-4 h-8 w-8" />
            <p className="text-xs uppercase tracking-luxe">{prediction.label}</p>
            <p className="mt-3 font-display text-5xl">
              {prediction.minutes}
              <span className="ml-2 text-lg text-muted-foreground">min</span>
            </p>
            <p className="mt-4 text-xs font-light text-muted-foreground">
              Estimated departure delay based on your flight details.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}