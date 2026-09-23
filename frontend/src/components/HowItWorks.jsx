function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Enter Flight Details",
      description:
        "Provide the airline, source, destination, journey date, departure time, arrival time, duration, stops and route.",
    },
    {
      number: "02",
      title: "Feature Engineering",
      description:
        "Raw flight information is transformed into machine-learning features such as journey date components, time components and duration.",
    },
    {
      number: "03",
      title: "Machine Learning",
      description:
        "The trained Random Forest pipeline processes the engineered features and identifies patterns learned from historical flight-price data.",
    },
    {
      number: "04",
      title: "Price Estimation",
      description:
        "The model returns an estimated ticket price in Indian Rupees based on the flight information provided.",
    },
  ];

  return (
    <section className="mt-10 rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
          How It Works
        </p>

        <h2 className="mt-2 text-2xl font-bold text-white">
          From flight details to price prediction
        </h2>

        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-400">
          FlightPredict combines feature engineering, preprocessing and
          machine learning to transform flight information into a ticket
          price estimate.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {steps.map((step) => (
          <div
            key={step.number}
            className="rounded-2xl border border-slate-800 bg-slate-950 p-6"
          >
            <div className="mb-5 flex items-center justify-between">
              <span className="text-3xl font-bold text-blue-400">
                {step.number}
              </span>

              <div className="h-px w-20 bg-slate-800" />
            </div>

            <h3 className="text-lg font-semibold text-white">
              {step.title}
            </h3>

            <p className="mt-3 text-sm leading-relaxed text-slate-400">
              {step.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;