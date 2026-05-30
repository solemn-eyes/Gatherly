export default function Hero() {
  return (
    <section className="bg-white py-24">
      <div className="max-w-7xl mx-auto px-6">

        <h1 className="text-6xl font-bold">
          Find it.
          <br />
          Plan it.
          <br />
          Fill it.
        </h1>

        <p className="mt-6 text-xl text-gray-600">
          Discover amazing events around you
          and create unforgettable experiences.
        </p>

        <div className="mt-8 flex gap-4">
          <button className="bg-[#E8593C] text-white px-6 py-3 rounded-xl">
            Explore Events
          </button>

          <button className="border px-6 py-3 rounded-xl">
            Host Event
          </button>
        </div>

      </div>
    </section>
  );
}
