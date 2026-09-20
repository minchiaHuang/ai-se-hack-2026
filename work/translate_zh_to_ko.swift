import Foundation
import Translation

struct TranslationEntry: Codable {
    let id: Int
    let text: String
}

@main
struct TranslateZhToKo {
    static func main() async throws {
        guard CommandLine.arguments.count == 3 else {
            fputs("Usage: translate_zh_to_ko <input.json> <output.json>\n", stderr)
            exit(2)
        }

        let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
        let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
        let entries = try JSONDecoder().decode([TranslationEntry].self, from: Data(contentsOf: inputURL))
        let session = TranslationSession(
            installedSource: Locale.Language(identifier: "zh-Hant"),
            target: Locale.Language(identifier: "ko")
        )
        try await session.prepareTranslation()

        var translations: [Int: String] = [:]
        for batch in entries.chunked(into: 12) {
            let markedSource = batch.map { "[[[\($0.id)]]]\($0.text)" }.joined(separator: "\n")
            let markedTarget = try await session.translate(markedSource).targetText
            let expression = try NSRegularExpression(pattern: "\\[\\[\\[(\\d+)\\]\\]\\]")
            let range = NSRange(markedTarget.startIndex..., in: markedTarget)
            let matches = expression.matches(in: markedTarget, range: range)
            for index in matches.indices {
                let match = matches[index]
                let id = Int((markedTarget as NSString).substring(with: match.range(at: 1)))!
                let start = Range(match.range, in: markedTarget)!.upperBound
                let end = index + 1 < matches.count ? Range(matches[index + 1].range, in: markedTarget)!.lowerBound : markedTarget.endIndex
                translations[id] = String(markedTarget[start..<end]).trimmingCharacters(in: .whitespacesAndNewlines)
            }
            for entry in batch where translations[entry.id] == nil {
                translations[entry.id] = try await session.translate(entry.text).targetText
            }
            print("Translated \(translations.count) of \(entries.count) segments.")
            fflush(stdout)
        }

        guard translations.count == entries.count else {
            throw NSError(domain: "KoreanTranslation", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing translated entries"])
        }
        let result = entries.map { TranslationEntry(id: $0.id, text: translations[$0.id]!) }
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        try encoder.encode(result).write(to: outputURL)
        print("Translated \(result.count) unique Chinese text segments to Korean.")
    }
}

extension Array {
    func chunked(into size: Int) -> [[Element]] {
        stride(from: 0, to: count, by: size).map { Array(self[$0..<Swift.min($0 + size, count)]) }
    }
}
