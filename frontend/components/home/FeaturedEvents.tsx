import EventCard from "../events/EventCard";

export default function FeaturedEvents() {
  return (
    <section className="max-w-7xl mx-auto px-6 py-20">
      <h2 className="text-3xl font-bold mb-10">
        Trending Events
      </h2>

      <div className="grid md:grid-cols-3 gap-6">

        <EventCard
          title="East Africa Jazz Night"
          location="Nakuru"
          date="June 6"
          price="KES 800"
        />

        <EventCard
          title="AI in Africa Meetup"
          location="Nakuru"
          date="June 13"
          price="Free"
        />

        <EventCard
          title="Rift Valley Marathon"
          location="Nakuru"
          date="June 22"
          price="KES 1200"
        />

      </div>
    </section>
  );
}
