import type { ArtifactsInfo } from "./ArtifactsInfo";
import axios from "axios";
import { api_endpoint } from "./api";

export class ArtifactsService {
  /**
   * View all artifacts
   */
  public static async getArtifacts(): Promise<ArtifactsInfo> {
    const response = await axios.get(`${api_endpoint}/register`);
      return response.data;
  }
}
