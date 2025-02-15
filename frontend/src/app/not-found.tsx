"use client";
import Image from "next/image";
import Button from "@/components/Button";

export default function NotFound() {
  return (
    /*<div className="h-screen w-min-1/2 align-center justify-center flex bg-gradient-to-t from-accent to-canvas-600 pr-20 pl-20">*/
    <div className=" grid h-4/5 grid-cols-1 lg:grid-cols-2 gap-10 p-10 lg:px-32">
      <div className="flex flex-col items-center justify-center ">
        <h3 className="text-6xl font-bold text-center text-brand-darkblue">404-Error</h3>
        <h2>Page Not Found</h2>
        <p className="pb-3 text-center text-brand-darkblue">
          The page you are looking for does not exist.
        </p>
        <Button variant="primary" onClick={() => window.open("/", "_self")}>
          Back to Home
        </Button>
      </div>

      <div className="flex flex-col items-center justify-center">
        <p className="text-8xl text-brand-darkblue">e-SparX</p>
        {/*<Image src="/favicon.ico" alt="404_icon" width={200} height={200} />*/}
        {/*<img src="favicon.ico" alt="404_icon" /> */}
      </div>
    </div>
  );
}
