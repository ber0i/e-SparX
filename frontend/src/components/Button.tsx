import React from "react";

interface ButtonProps {
  children: React.ReactNode;
  variant: "primary" | "secondary" | "disabled";
  onClick?: () => void;
  className?: string;
  type?: "button" | "submit" | "reset";
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant,
  onClick,
  className = "",
  type = "button",
}) => {
  const baseStyle =
    "font-semibold py-2 px-5 rounded transition ease-in duration-200 mx-0.5 border-2";
  const variants = {
    primary: `bg-primary hover:bg-primary-shade border-primary-shade text-brand-white ${baseStyle}`,
    secondary: `bg-secondary hover:bg-secondary-shade border-secondary-shade text-brand-white ${baseStyle}`,
    disabled: `bg-brand-smoke text-brand-gray cursor-not-allowed opacity-50 ${baseStyle}`,
  };

  // giving disabled variant the disabled attribute
  const isDisabled = variant === "disabled";

  return (
    <button
      type={type}
      className={`${variants[variant]} ${className}`}
      onClick={onClick}
      disabled={isDisabled}
    >
      {children}
    </button>
  );
};

export default Button;
