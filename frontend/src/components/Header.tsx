import Image from "next/image";
import tumLogo from "../../public/tum-logo.png";
import esparxLogo from "../../public/esparx-logo.png";

const Header = () => {
  const pages = [
    { url: "/artifacts", title: "Artifacts" },
    { url: "/pipelines", title: "Pipelines" },
    { url: "/global", title: "Global Artifact Graph" },
  ];
  //  let mobile_menu_open = false;

  return (
    <div className="bg-brand-darkblue">
      <nav
        className="mx-auto flex items-center justify-between p-6 lg:px-8"
        aria-label="Global"
      >

        {/* Logo */}
        <div className="mx-auto flex items-start space-x-4 lg:flex-1">
          <a href="/">
            <Image
              src={tumLogo}
              alt="e-SparX Logo"
              width={80}
              height={80}
              style={{paddingTop: "5px"}}
            />
          </a>
          <a href="/">
            <Image
              src={esparxLogo}
              alt="e-SparX Logo"
              width={140}
              height={140}
              style={{paddingTop: "5px"}}
            />
          </a>
        </div>

        {/* Navigation Links */}
        <div className="group flex lg:hidden">
          <button
            type="button"
            className="peer -m-2.5 inline-flex items-center justify-center rounded-md p-2 text-brand-white group-hover:text-brand-linkhover group-focus-within:text-brand-darkblue"
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
          <ul className="invisible group-focus-within:visible group-hover:visible absolute bg-brand-darkblue rounded-lg shadow-xl border border-brand-darkblue -translate-x-[calc(100%-24px)] translate-y-[24px] overflow-hidden">
            {pages.map(({ url, title }) => (
              <li key={url} className="p-2">
                <a href={url} className="font-semibold text-brand-white hover:text-brand-linkhover">
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
              className="text-lg leading-6 text-brand-white hover:text-brand-linkhover"
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
