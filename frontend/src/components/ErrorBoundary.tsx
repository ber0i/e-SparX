import React from "react";
import Button from "@/components/Button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";

interface ErrorBoundaryState {
  hasError: boolean;
}
interface Props {
  suggestedFix: string;
  children: React.ReactNode;
}

//ErrorBoundary component which you can wrap arround your components to catch errors like a try-catch block
// example: <ErrorBoundary suggestedFix="Select the right database">
class ErrorBoundary extends React.Component<Props, ErrorBoundaryState> {
  constructor(props: Props) {
    super(props);

    // Define a state variable to track whether is an error or not
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error: any) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }
  componentDidCatch(error: any, errorInfo: any) {
    // You can use your own error logging service here
    console.log({ error, errorInfo });
  }
  render() {
    // Check if the error is thrown
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div className="flex flex-col border border-secondary items-center shadow rounded-2xl p-7 text-center bg-accent h-full justify-center">
          <FontAwesomeIcon
            className="text-primary fa-2xl text-center mb-4"
            icon={faTriangleExclamation}
          />
          <h2>Oops, there is an error!</h2>

          {this.props.suggestedFix && (
            <p className="text-contrast text-sm mb-4">
              {this.props.suggestedFix}
            </p>
          )}
          <p className="text-contrast text-sm mb-4">
            Or check the error-log at the bottom left corner.
          </p>
          <Button
            variant="primary"
            onClick={() => {
              this.setState({ hasError: false });
              window.location.reload();
            }}
          >
            Try again
          </Button>
        </div>
      );
    }
    // otherwise render the children
    else {
      return this.props.children;
    }
  }
}

export default ErrorBoundary;
