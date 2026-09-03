import Foundation
import AVFoundation
import Vision
import CoreGraphics

guard CommandLine.arguments.count >= 2 else {
    fputs("Usage: ocr_hardsub_video <video> [interval_seconds]\n", stderr)
    exit(2)
}

let videoURL = URL(fileURLWithPath: CommandLine.arguments[1])
let interval = CommandLine.arguments.count >= 3 ? (Double(CommandLine.arguments[2]) ?? 2.0) : 2.0
guard interval > 0 else {
    fputs("interval_seconds must be greater than zero\n", stderr)
    exit(2)
}

let asset = AVURLAsset(url: videoURL)
let duration = CMTimeGetSeconds(asset.duration)
guard duration.isFinite && duration > 0 else {
    fputs("Could not read video duration\n", stderr)
    exit(3)
}

let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
generator.requestedTimeToleranceBefore = CMTime(seconds: 0.25, preferredTimescale: 600)
generator.requestedTimeToleranceAfter = CMTime(seconds: 0.25, preferredTimescale: 600)

func recognize(_ image: CGImage) -> String {
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    request.usesLanguageCorrection = true
    request.minimumTextHeight = 0.012
    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    do {
        try handler.perform([request])
    } catch {
        return ""
    }
    let observations = request.results ?? []
    let ordered = observations.sorted {
        if abs($0.boundingBox.midY - $1.boundingBox.midY) > 0.02 {
            return $0.boundingBox.midY > $1.boundingBox.midY
        }
        return $0.boundingBox.minX < $1.boundingBox.minX
    }
    return ordered.compactMap { $0.topCandidates(1).first?.string }
        .joined(separator: " | ")
        .replacingOccurrences(of: "\n", with: " ")
}

var previous = ""
var second = 0.0
while second < duration {
    autoreleasepool {
        let requested = CMTime(seconds: second, preferredTimescale: 600)
        if let image = try? generator.copyCGImage(at: requested, actualTime: nil) {
            let text = recognize(image)
            if !text.isEmpty && text != previous {
                let record: [String: Any] = ["t": second, "text": text]
                if let data = try? JSONSerialization.data(withJSONObject: record),
                   let line = String(data: data, encoding: .utf8) {
                    print(line)
                }
                previous = text
            }
        }
    }
    second += interval
}

