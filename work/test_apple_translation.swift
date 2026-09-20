import Foundation
import Translation

@main
struct TestAppleTranslation {
    static func main() async {
        let source = Locale.Language(identifier: "zh-Hant")
        let target = Locale.Language(identifier: "ko")
        let availability = LanguageAvailability()
        print("status=\(await availability.status(from: source, to: target))")
        do {
            let session = TranslationSession(installedSource: source, target: target)
            let response = try await session.translate("社會企業需要可驗證的影響衡量。")
            print("translation=\(response.targetText)")
        } catch {
            print("translation_error=\(error.localizedDescription)")
        }
    }
}
