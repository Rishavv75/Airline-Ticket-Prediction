import { useState } from "react";

function FlightForm({ metadata, onPrediction, onError }) {
  const [formData, setFormData] = useState({
    airline: metadata.airlines[0]?.value ?? metadata.airlines[0] ?? "",
    date_of_journey: "",
    source: metadata.sources[0]?.value ?? metadata.sources[0] ?? "",
    destination:
      metadata.destinations[0]?.value ?? metadata.destinations[0] ?? "",
    route: "",
    departure_time: "",
    arrival_time: "",
    duration: "",
    total_stops: metadata.stops[0]?.value ?? metadata.stops[0] ?? "non-stop",
    additional_info:
      metadata.additional_info[0]?.value ??
      metadata.additional_info[0] ??
      "No info",
  });

  const [loading, setLoading] = useState(false);

  function getOptionValue(option) {
    if (typeof option === "string") {
      return option;
    }

    return option?.value ?? option?.label ?? "";
  }

  function getOptionLabel(option) {
    if (typeof option === "string") {
      return option;
    }

    return option?.label ?? option?.value ?? "";
  }

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    onError("");

    try {
    console.log("Sending flight data:", formData);
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
  console.error("Backend error:", data);

  let errorMessage = "Prediction failed";

  if (Array.isArray(data.detail)) {
    errorMessage = data.detail
      .map((error) => {
        const field = Array.isArray(error.loc)
          ? error.loc.join(".")
          : "unknown field";

        return `${field}: ${error.msg}`;
      })
      .join("\n");
  } else if (typeof data.detail === "string") {
    errorMessage = data.detail;
  }

  throw new Error(errorMessage);
}
      onPrediction(data);
    } catch (error) {
      console.error(error);
      onError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl"
    >
      {/* HEADER */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold">
          Flight Details
        </h2>

        <p className="mt-2 text-sm text-slate-400">
          Enter the details of your flight to estimate the ticket price.
        </p>
      </div>

      {/* FORM GRID */}
      <div className="grid gap-5 md:grid-cols-2">

        {/* AIRLINE */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Airline
          </label>

          <select
            name="airline"
            value={formData.airline}
            onChange={handleChange}
            className="input"
            required
          >
            {metadata.airlines.map((airline, index) => {
              const value = getOptionValue(airline);
              const label = getOptionLabel(airline);

              return (
                <option key={`${value}-${index}`} value={value}>
                  {label}
                </option>
              );
            })}
          </select>
        </div>

        {/* SOURCE */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Source
          </label>

          <select
            name="source"
            value={formData.source}
            onChange={handleChange}
            className="input"
            required
          >
            {metadata.sources.map((source, index) => {
              const value = getOptionValue(source);
              const label = getOptionLabel(source);

              return (
                <option key={`${value}-${index}`} value={value}>
                  {label}
                </option>
              );
            })}
          </select>
        </div>

        {/* DESTINATION */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Destination
          </label>

          <select
            name="destination"
            value={formData.destination}
            onChange={handleChange}
            className="input"
            required
          >
            {metadata.destinations.map((destination, index) => {
              const value = getOptionValue(destination);
              const label = getOptionLabel(destination);

              return (
                <option key={`${value}-${index}`} value={value}>
                  {label}
                </option>
              );
            })}
          </select>
        </div>

        {/* JOURNEY DATE */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Journey Date
          </label>

          <input
            type="date"
            name="date_of_journey"
            value={formData.date_of_journey}
            onChange={handleChange}
            className="input"
            required
          />
        </div>

        {/* DEPARTURE TIME */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Departure Time
          </label>

          <input
            type="time"
            name="departure_time"
            value={formData.departure_time}
            onChange={handleChange}
            className="input"
            required
          />
        </div>

        {/* ARRIVAL TIME */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Arrival Time
          </label>

          <input
            type="time"
            name="arrival_time"
            value={formData.arrival_time}
            onChange={handleChange}
            className="input"
            required
          />
        </div>

        {/* DURATION */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Duration
          </label>

          <input
            type="text"
            name="duration"
            value={formData.duration}
            onChange={handleChange}
            placeholder="e.g. 2h 50m"
            className="input"
            required
          />
        </div>

        {/* STOPS */}
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Stops
          </label>

          <select
            name="total_stops"
            value={formData.total_stops}
            onChange={handleChange}
            className="input"
            required
          >
            {metadata.stops.map((stop, index) => {
              const value = getOptionValue(stop);
              const label = getOptionLabel(stop);

              return (
                <option key={`${value}-${index}`} value={value}>
                  {label}
                </option>
              );
            })}
          </select>
        </div>

        {/* ROUTE */}
        <div className="md:col-span-2">
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Route
          </label>

          <input
            type="text"
            name="route"
            value={formData.route}
            onChange={handleChange}
            placeholder="e.g. BLR → DEL"
            className="input"
            required
          />

          <p className="mt-2 text-xs text-slate-500">
            Example: BLR → BOM → DEL
          </p>
        </div>

        {/* ADDITIONAL INFORMATION */}
        <div className="md:col-span-2">
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Additional Information
          </label>

          <select
            name="additional_info"
            value={formData.additional_info}
            onChange={handleChange}
            className="input"
          >
            {metadata.additional_info.map((info, index) => {
              const value = getOptionValue(info);
              const label = getOptionLabel(info);

              return (
                <option key={`${value}-${index}`} value={value}>
                  {label}
                </option>
              );
            })}
          </select>
        </div>

      </div>

      {/* SUBMIT BUTTON */}
      <button
        type="submit"
        disabled={loading}
        className="mt-8 w-full rounded-xl bg-blue-500 px-6 py-4 font-semibold text-white transition hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Predicting..." : "Predict Ticket Price"}
      </button>
    </form>
  );
}

export default FlightForm;