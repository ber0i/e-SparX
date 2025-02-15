// Function to perform topological sort (enabling DAGs)
export const topologicalSort = (nodesMap: Map<string, string[]>) => {
  const sortedNodes: string[] = [];
  const visited: Set<string> = new Set();
  const tempMark: Set<string> = new Set();
  const nodeLevels: Map<string, number> = new Map();

  const visit = (node: string, level: number, inLoop: boolean) => {
    if (tempMark.has(node)) return; // Ignore temporary marked nodes (prevents cycles)
    if (!visited.has(node) || inLoop) {
      tempMark.add(node); // Mark the node temporarily
      const dependencies = nodesMap.get(node) || [];
      dependencies.forEach((dep) => visit(dep, level + 1, true));
      if (!visited.has(node)) {
        visited.add(node); // Mark as permanently visited
        sortedNodes.push(node); // Add node to sorted result
      }
      tempMark.delete(node);
      nodeLevels.set(node, Math.max(level, nodeLevels.get(node) || 0));
    }
  };

  nodesMap.forEach((_, node) => {
    if (!visited.has(node)) {
      visit(node, 0, false);
    }
  });
  return { sortedNodes, nodeLevels };
};
