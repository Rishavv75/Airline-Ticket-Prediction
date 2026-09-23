function PredictionCard({ prediction }) {
  if (!prediction) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
        <div className="mb-6">
          <p className="text-sm font-semibold uppercase tracking-widest text-slate-500">
            Prediction
          </p>

          <h2 className="mt-2 text-2xl font-bold text-white">
            Your estimated price
          </h2>
        </div>

        <div className="flex min-h-65 items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-950">
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-500/10 text-2xl">
              ✈️
            </div>

            <p className="text-sm text-slate-400">
              Enter your flight details
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Your prediction will appear here
            </p>
          </div>
        </div>
      </div>
    );
  }

  const price = Number(prediction.predicted_price);

  const formattedPrice = new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
  }).format(price);

  const flight = prediction.flight;

  return (
    <div className="overflow-hidden rounded-3xl border border-blue-500/20 bg-slate-900 shadow-2xl">

      {/* Header */}
      <div className="border-b border-slate-800 p-6">
        <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
          Prediction Result
        </p>

        <h2 className="mt-2 text-2xl font-bold text-white">
          Estimated Ticket Price
        </h2>
      </div>

      {/* Price */}
      <div className="p-6">

        <div className="rounded-2xl bg-slate-950 p-6 text-center">

          <p className="text-sm text-slate-500">
            Estimated fare
          </p>

          <div className="mt-3">
            <span className="text-4xl font-extrabold tracking-tight text-white">
              ₹{formattedPrice}
            </span>
          </div>

          <p className="mt-2 text-xs text-slate-500">
            Indian Rupees
          </p>

        </div>

        {/* Flight Summary */}
        {flight && (
          <div className="mt-6">

            <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-blue-400">
              Flight Summary
            </p>

            <div className="space-y-3">

              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-sm text-slate-500">
                  Airline
                </span>

                <span className="text-right text-sm font-medium text-slate-200">
                  {flight.airline}
                </span>
              </div>

              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-sm text-slate-500">
                  Route
                </span>

                <span className="text-right text-sm font-medium text-slate-200">
                  {flight.route}
                </span>
              </div>

              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-sm text-slate-500">
                  Source
                </span>

                <span className="text-right text-sm font-medium text-slate-200">
                  {flight.source}
                </span>
              </div>

              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-sm text-slate-500">
                  Destination
                </span>

                <span className="text-right text-sm font-medium text-slate-200">
                  {flight.destination}
                </span>
              </div>

              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-sm text-slate-500">
                  Stops
                </span>

                <span className="text-right text-sm font-medium text-slate-200">
                  {flight.total_stops}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-500">
                  Duration
                </span>

                <span className="text-right text-sm font-medium text-slate-200">
                  {flight.duration}
                </span>
              </div>

            </div>
          </div>
        )}

        {/* Model information */}
        <div className="mt-6">

          <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Model Information
          </p>

          <div className="space-y-3">

            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <span className="text-sm text-slate-500">
                Model
              </span>

              <span className="text-sm font-medium text-slate-200">
                {prediction.model || "Random Forest"}
              </span>
            </div>

            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <span className="text-sm text-slate-500">
                Version
              </span>

              <span className="text-sm font-medium text-slate-200">
                {prediction.model_version || "1.0"}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">
                Currency
              </span>

              <span className="text-sm font-medium text-slate-200">
                {prediction.currency || "INR"}
              </span>
            </div>

          </div>

        </div>

        {/* Disclaimer */}
        <div className="mt-6 rounded-xl border border-yellow-500/10 bg-yellow-500/5 p-4">

          <p className="text-xs leading-relaxed text-slate-500">
            This is a machine learning estimate based on the flight
            information provided. Actual ticket prices may vary.
          </p>

        </div>

      </div>
    </div>
  );
}

export default PredictionCard;