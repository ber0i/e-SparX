"use client";

export default function Imprint() {
  return (
    <div className="p-5 max-w-3xl mx-auto text-gray-800">
      <h1 className="text-2xl font-bold mb-4">Impressum</h1>

      <p className="mb-2">
        Angaben gemäß § 5 TMG
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Herausgeber</h2>

      <p className="mb-4">
        Technische Universität München <br />
        Arcisstraße 21 <br />
        80333 München <br />
        Deutschland
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Inhaltlich verantwortlich</h2>

      <p className="mb-4">
        Prof. Dr. rer. pol. Christoph Goebel <br />
        Arcisstraße 21 <br />
        80333 München <br />
        Deutschland
      </p>

      <p className="mb-4">
        E-Mail: christoph.goebel(at)tum.de
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Haftungsausschluss</h2>

      <p className="mb-4">
        Diese Website dient ausschließlich nicht-kommerziellen Zwecken im Rahmen eines Forschungsprojekts.
        Für die Inhalte externer Links übernehmen wir keine Haftung. Für den Inhalt der verlinkten Seiten
        sind ausschließlich deren Betreiber verantwortlich.
      </p>

    </div>
  );
}

