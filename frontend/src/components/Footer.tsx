// components/Footer.tsx
export default function Footer() {
  return (
    <footer className="mt-16 px-4 py-8 bg-brand-tablecolor text-center text-sm text-brand-darkblue">
      <p className="mb-2">
        For more information on the project, check out{" "}
        <a
          href="https://doi.org/10.1145/3679240.3734617"
          className="text-brand-tumblue underline hover:text-brand-darkblue"
          target="_blank"
          rel="noopener noreferrer"
        >
          this publication
        </a>
        !
      </p>
      <div className="space-x-4">
        <a
          href="/privacy"
          className="text-brand-tumblue hover:text-brand-darkblue underline"
        >
          Privacy Policy
        </a>
        <span>|</span>
        <a
          href="/imprint"
          className="text-brand-tumblue hover:text-brand-darkblue underline"
        >
          Imprint
        </a>
        <span>|</span>
        <a
          href="https://gitlab.lrz.de/energy-management-technologies-public/e-sparx"
          className="text-brand-tumblue hover:text-brand-darkblue underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitLab
        </a>
      </div>
    </footer>
  );
}
