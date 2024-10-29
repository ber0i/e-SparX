import clsx from "clsx";
import Image from "next/legacy/image";

const Header = () => {
  const pages = [
    { url: "/artifacts", title: "Artifacts" },
    { url: "/pipelines", title: "Pipelines" },
    { url: "/global", title: "Global Artifact Graph" },
  ];
  //  let mobile_menu_open = false;

  return (
    <div className="bg-accent dark:bg-brand-gray">
      <nav
        className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8"
        aria-label="Global"
      >
        <div className="flex lg:flex-1">
          <a href="/" className="-m-1.5 p-1.5">
            <span className="sr-only">EDL</span>
            <Image
              src="/favicon.ico"
              alt="EDL Logo"
              width={32}
              height={32}
              layout="fixed"
            />
          </a>
        </div>
        <div className="group flex lg:hidden">
          <button
            type="button"
            className="peer -m-2.5 inline-flex items-center justify-center rounded-md p-2 text-contrast group-hover:text-primary group-focus-within:text-primary"
          >
            <span className="sr-only">Open main menu</span>
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
              />
            </svg>
          </button>
          <ul className="invisible group-focus-within:visible group-hover:visible absolute bg-canvas rounded-lg shadow-xl border border-brand-smoke dark:border-primary -translate-x-[calc(100%-24px)] translate-y-[24px] overflow-hidden">
            {pages.map(({ url, title }) => (
              <li key={url} className="hover:bg-accent p-2">
                <a href={url} className="font-semibold text-contrast">
                  {title}
                </a>
              </li>
            ))}
          </ul>
        </div>
        <div className="hidden focus-within:visible lg:flex lg:gap-x-12">
          {pages.map(({ url, title }) => (
            <a
              key={url}
              href={url}
              className="text-sm font-semibold leading-6 text-contrast"
            >
              {title}
            </a>
          ))}
        </div>
      </nav>
    </div>
  );
};

export default Header;
