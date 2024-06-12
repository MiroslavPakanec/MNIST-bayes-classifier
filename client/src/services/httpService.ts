import { usePixelStore } from "@/stores/pixelStore";

export class HttpService {
    private pixelStore = usePixelStore()

    public getPixelsJson(): string {
        const pixels: number[][] = this.pixelStore.pixels
        const inverted: number[][] = this.pixelStore.invert(pixels)
        const flattened: number[] = this.pixelStore.flatten(inverted)
        return JSON.stringify(flattened)
    }

    public async predictDigit(): Promise<number> {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'POST'
        const body: string = this.getPixelsJson()
        console.log(body)
        const options = { headers, method, body }
        const url: string = process.env.VUE_APP_PREDICT_ENDPOINT_URL
        const response: any = await fetch(url, options)
        if (response?.ok) return response.json['prediction']
        else alert('error')
        return 0
    }
}