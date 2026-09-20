import { useEffect, useState } from "react";
import { getMetadata } from "./services/api";
import FlightForm from "./components/FlightForm";
import PredictionCard from "./components/PredictionCard";

function App() {
  const [metadata, setMetadata] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMetadata() {
      try {
        const data = await getMetadata();
        setMetadata(data);
      } catch (err) {
        console.error(err);
        setError("Unable to connect to the prediction API.");
      } finally {
        setLoading(false);
      }
    }

    loadMetadata();
  }, []);

  function handlePrediction(data) {
    setPrediction(data);
    setError("");
  }

  function handleError(message) {
    setError(message);
    setPrediction(null);
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <p className="text-slate-400">
          Loading prediction system...
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <header className="border-b border-slate-800">
        <div className="mx-auto max-w-6xl px-6 py-5">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold">
                FlightPredict
              </h1>

              <p className="text-xs text-slate-500">
                ML-powered airline price estimation
              </p>
            </div>

            <div className="rounded-full border border-green-500/30 bg-green-500/10 px-3 py-1 text-xs text-green-400">
              API Online
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-12">

        <section className="mb-10">
          <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Airline Intelligence
          </p>

          <h2 className="max-w-3xl text-4xl font-bold tracking-tight md:text-5xl">
            Predict your flight ticket price
            <span className="text-blue-400"> before you book.</span>
          </h2>

          <p className="mt-5 max-w-2xl text-lg leading-relaxed text-slate-400">
            Enter your flight details and our machine learning model will
            estimate the expected ticket price.
          </p>
        </section>

        {error && (
          <div className="mb-6 rounded-xl border border-red-900 bg-red-950/40 p-4">
            <p className="text-sm text-red-400">
              {error}
            </p>
          </div>
        )}

        {metadata && (
          <div className="grid gap-8 lg:grid-cols-[1fr_380px]">

            <FlightForm
              metadata={metadata}
              onPrediction={handlePrediction}
              onError={handleError}
            />

            <div className="lg:sticky lg:top-8 lg:self-start">
              <PredictionCard prediction={prediction} />
            </div>

          </div>
        )}

      </main>

      <footer className="border-t border-slate-800">
        <div className="mx-auto max-w-6xl px-6 py-6">
          <p className="text-center text-xs text-slate-600">
            Airline Ticket Price Prediction • Machine Learning Project
          </p>
        </div>
      </footer>

    </div>
  );
}

export default App;