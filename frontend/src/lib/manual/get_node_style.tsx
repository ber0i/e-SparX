export const getNodeStyle = (artifact_type: string) => {
  if (artifact_type === "dataset") {
    return { backgroundColor: "rgb(63, 161, 241)" }; // Blue background, black text
  }
  if (artifact_type === "code") {
    return { backgroundColor: "gray", color: "white" }; // Gray background, white text
  }
  if (artifact_type === "model") {
    return { backgroundColor: "rgb(12, 167, 137)", color: "black" }; // Green background, black text
  }
  if (artifact_type === "hyperparameters") {
    return { backgroundColor: "rgba(12, 167, 137, 0.6)" }; // Light green background, black text
  }
  if (artifact_type === "parameters") {
    return { backgroundColor: "rgba(12, 167, 137, 0.6)" }; // Light green background, black text
  }
  if (artifact_type === "results") {
    return { backgroundColor: "rgba(8, 102, 84, 0.8)", color: "white" }; // Dark green background, white text
  }
  return { backgroundColor: "white" }; // White background, black text
};
