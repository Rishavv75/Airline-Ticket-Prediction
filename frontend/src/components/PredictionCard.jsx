function PredictionCard({ prediction }) {
  if (!prediction) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-700 bg-slate-900/50 p-8 text-center">
        <p className="text-slate-500">
          Your predicted ticket price will appear here.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-3xl border border-blue-500/30 bg-blue-500/10 p-8 text-center">
      <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
        Estimated Ticket Price
      </p>

      <div className="mt-5">
        <span className="text-5xl font-bold tracking-tight">
          ₹{Number(prediction.predicted_price).toLocaleString("en-IN", {
            maximumFractionDigits: 2,
          })}
        </span>
      </div>

      <p className="mt-4 text-sm text-slate-400">
        This price is an ML-based estimate, not a live airline fare.
      </p>
    </div>
  );
}

export default PredictionCard;