function ModelInsights() {
  const features = [
    {
      name: "Jet Airways Business",
      importance: 14.0521,
    },
    {
      name: "Total Stops",
      importance: 13.0821,
    },
    {
      name: "Duration",
      importance: 6.1575,
    },
    {
      name: "Jet Airways",
      importance: 5.0017,
    },
    {
      name: "In-flight meal not included",
      importance: 4.9726,
    },
  ];

  const maxImportance = features[0].importance;

  return (
    <section className="mt-8 rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">

      {/* Header */}
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
          Model Insights
        </p>

        <h2 className="mt-2 text-2xl font-bold text-white">
          What influences the model?
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-slate-400">
          These are the most important features learned by the Random Forest
          model across the training data.
        </p>
      </div>

      {/* Feature importance */}
      <div>
        <h3 className="mb-5 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Global Feature Importance
        </h3>

        <div className="space-y-5">
          {features.map((feature) => {
            const width =
              (feature.importance / maxImportance) * 100;

            return (
              <div key={feature.name}>

                <div className="mb-2 flex items-center justify-between gap-4">

                  <span className="text-sm text-slate-300">
                    {feature.name}
                  </span>

                  <span className="text-sm font-semibold text-blue-400">
                    {feature.importance.toFixed(2)}%
                  </span>

                </div>

                <div className="h-2 overflow-hidden rounded-full bg-slate-800">

                  <div
                    className="h-full rounded-full bg-blue-500 transition-all duration-700"
                    style={{ width: `${width}%` }}
                  />

                </div>

              </div>
            );
          })}
        </div>
      </div>

      {/* Divider */}
      <div className="my-8 border-t border-slate-800" />

      {/* Model performance */}
      <div>

        <h3 className="mb-5 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Model Performance
        </h3>

        <div className="grid gap-4 sm:grid-cols-3">

          <div className="rounded-2xl bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wider text-slate-500">
              MAE
            </p>

            <p className="mt-2 text-xl font-bold text-white">
              ₹569.76
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Mean Absolute Error
            </p>
          </div>

          <div className="rounded-2xl bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wider text-slate-500">
              RMSE
            </p>

            <p className="mt-2 text-xl font-bold text-white">
              ₹1,451.92
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Root Mean Squared Error
            </p>
          </div>

          <div className="rounded-2xl bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wider text-slate-500">
              R²
            </p>

            <p className="mt-2 text-xl font-bold text-white">
              90.22%
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Explained variance
            </p>
          </div>

        </div>

      </div>

      {/* Disclaimer */}
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950/50 p-4">

        <p className="text-xs leading-relaxed text-slate-500">
          Feature importance represents the model's global behavior across
          the training data. It should not be interpreted as the individual
          causal contribution to a single prediction.
        </p>

      </div>

    </section>
  );
}

export default ModelInsights;