import apiClient from './client';

export type NodeType = 'ai_system' | 'workflow' | 'audit';
export type EdgeType = 'uses' | 'depends_on' | 'feeds_into' | 'integration' | 'escalates_to';

export interface DependencyNode {
  id: string;
  organization_id: string;
  node_type: NodeType;
  ai_system_id: string | null;
  workflow_id: string | null;
  audit_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface DependencyNodeCreate {
  node_type: NodeType;
  ai_system_id?: string | null;
  workflow_id?: string | null;
  audit_id?: string | null;
}

export interface DependencyEdge {
  id: string;
  organization_id: string;
  source_node_id: string;
  target_node_id: string;
  edge_type: EdgeType;
  created_at: string;
  updated_at: string;
}

export interface DependencyEdgeCreate {
  source_node_id: string;
  target_node_id: string;
  edge_type: EdgeType;
}

export const dependencyMapApi = {
  // Nodes
  listNodes: async (): Promise<DependencyNode[]> => {
    const response = await apiClient.get('/api/dependency-map/nodes');
    return response.data;
  },

  getOrCreateNode: async (data: DependencyNodeCreate): Promise<DependencyNode> => {
    const response = await apiClient.post('/api/dependency-map/nodes/get-or-create', data);
    return response.data;
  },

  createNode: async (data: DependencyNodeCreate): Promise<DependencyNode> => {
    const response = await apiClient.post('/api/dependency-map/nodes', data);
    return response.data;
  },

  getNode: async (id: string): Promise<DependencyNode> => {
    const response = await apiClient.get(`/api/dependency-map/nodes/${id}`);
    return response.data;
  },

  deleteNode: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/dependency-map/nodes/${id}`);
  },

  // Edges
  listEdges: async (): Promise<DependencyEdge[]> => {
    const response = await apiClient.get('/api/dependency-map/edges');
    return response.data;
  },

  createEdge: async (data: DependencyEdgeCreate): Promise<DependencyEdge> => {
    const response = await apiClient.post('/api/dependency-map/edges', data);
    return response.data;
  },

  getEdge: async (id: string): Promise<DependencyEdge> => {
    const response = await apiClient.get(`/api/dependency-map/edges/${id}`);
    return response.data;
  },

  deleteEdge: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/dependency-map/edges/${id}`);
  },
};
