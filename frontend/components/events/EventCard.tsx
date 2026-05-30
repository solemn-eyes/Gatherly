interface EventCardProps {
  title: string;
  location: string;
  date: string;
  price: string;
}

export default function EventCard({
  title,
  location,
  date,
  price,
}: EventCardProps) {
  return (
    <div className="rounded-xl shadow-md overflow-hidden bg-white">
      <div className="h-40 bg-orange-200"></div>

      <div className="p-4">
        <h3 className="font-semibold text-lg">
          {title}
        </h3>

        <p>{location}</p>
        <p>{date}</p>

        <div className="mt-4 flex justify-between">
          <span>{price}</span>

          <button className="bg-[#E8593C] text-white px-4 py-2 rounded-lg">
            Book
          </button>
        </div>
      </div>
    </div>
  );
}
