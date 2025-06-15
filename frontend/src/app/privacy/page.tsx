"use client";

export default function PrivacyPolicy() {
  return (
    <div className="p-5 max-w-3xl mx-auto text-gray-800">
      <h1 className="text-2xl font-bold mb-4">Datenschutzerklärung</h1>

      <p className="mb-4">
        Der Schutz Ihrer persönlichen Daten ist uns ein besonderes Anliegen. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Allgemeine Hinweise</h2>
      <p className="mb-4">
        Diese Website wird im Rahmen eines nicht-kommerziellen Forschungsprojekts betrieben. Ein Besuch der Website ist ohne Angabe personenbezogener Daten möglich. Es besteht jedoch die Möglichkeit, Inhalte beizutragen, wobei Nutzende freiwillig Informationen angeben können.
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Server-Log-Dateien</h2>
      <p className="mb-4">
        Der Hosting-Provider dieser Website erhebt und speichert automatisch Informationen in sogenannten Server-Log-Dateien, die Ihr Browser automatisch übermittelt. Dies umfasst insbesondere:
      </p>
      <ul className="list-disc list-inside mb-4">
        <li>IP-Adresse</li>
        <li>Datum und Uhrzeit der Serveranfrage</li>
        <li>Browsertyp und Browserversion</li>
        <li>Verwendetes Betriebssystem</li>
        <li>Referrer URL</li>
      </ul>
      <p className="mb-4">
        Diese Daten sind nicht bestimmten Personen zuordenbar. Eine Zusammenführung dieser Daten mit anderen Datenquellen wird nicht vorgenommen. Wir behalten uns vor, diese Daten nachträglich zu prüfen, wenn uns konkrete Anhaltspunkte für eine rechtswidrige Nutzung bekannt werden.
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Beiträge und Inhalte von Nutzenden</h2>
      <p className="mb-4">
        Nutzende können Inhalte auf dieser Website beitragen. Die Angabe personenbezogener Daten ist dabei nicht erforderlich, jedoch können freiwillig solche Daten preisgegeben werden. Für alle veröffentlichten Inhalte sind die jeweiligen Nutzenden selbst verantwortlich.
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Verwendung von Webfonts und Icons</h2> 
      <p className="mb-4">
        Diese Website verwendet lokal eingebundene Schriftarten von Google Fonts sowie Icons von Font Awesome. Es werden dabei keine Daten an externe Server von Google oder Dritten übermittelt.
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Kontaktaufnahme</h2>
      <p className="mb-4">
        Bei Fragen zum Datenschutz wenden Sie sich bitte an die im{" "}
        <a href="/imprint" className="text-brand-tumblue hover:text-brand-darkblue underline">Impressum</a> angegebene verantwortliche Person.
      </p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Ihre Rechte</h2>
      <p className="mb-4">
        Sie haben jederzeit das Recht auf Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und Empfänger sowie den Zweck der Datenverarbeitung. Außerdem haben Sie ein Recht auf Berichtigung, Sperrung oder Löschung dieser Daten.
      </p>
    </div>
  );
}
