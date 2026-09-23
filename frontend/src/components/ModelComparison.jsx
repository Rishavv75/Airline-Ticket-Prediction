function ModelComparison() {
  return (
    <section className="mt-10 rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
          Model Evaluation
        </p>

        <h2 className="mt-2 text-2xl font-bold text-white">
          Random Forest vs XGBoost
        </h2>

        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-400">
          Both models were evaluated on the same flight-price prediction
          problem using the same engineered dataset.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-slate-800 text-sm text-slate-400">
              <th className="px-4 py-4 font-medium">
                Model
              </th>

              <th className="px-4 py-4 font-medium">
                MAE
              </th>

              <th className="px-4 py-4 font-medium">
                RMSE
              </th>

              <th className="px-4 py-4 font-medium">
                R²
              </th>
            </tr>
          </thead>

          <tbody>
            <tr className="border-b border-slate-800">
              <td className="px-4 py-5 font-semibold text-white">
                Random Forest
              </td>

              <td className="px-4 py-5 text-slate-300">
                ₹569.76
              </td>

              <td className="px-4 py-5 text-slate-300">
                ₹1,451.92
              </td>

              <td className="px-4 py-5 text-slate-300">
                0.9022
              </td>
            </tr>

            <tr>
              <td className="px-4 py-5 font-semibold text-white">
                XGBoost
              </td>

              <td className="px-4 py-5 text-slate-300">
                ₹746.99
              </td>

              <td className="px-4 py-5 text-slate-300">
                ₹1,289.40
              </td>

              <td className="px-4 py-5 text-slate-300">
                0.9229
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950 p-5">
        <p className="text-sm leading-relaxed text-slate-400">
          On the evaluated test set, Random Forest produced a lower MAE,
          while XGBoost produced a lower RMSE and higher R². These metrics
          capture different aspects of prediction error, so they should be
          interpreted together.
        </p>
      </div>
    </section>
  );
}

export default ModelComparison;