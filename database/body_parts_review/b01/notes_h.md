# Notes, agent h (batch b01): humerus, radius, ulna, hip bone, patella

All five files pass `--check` (ok). Main source: Gray's 1918 on PubAnnotation, docs 51 (humerus),
52 (ulna), 53 (radius), 57 (hip bone), 60 (patella), and 17 (general classification of bones).
I took the clinical lines from MedlinePlus (arm, shoulder, elbow, wrist, hip) and NIAMS Sports Injuries.

## Blank fields
- radius: `aliases` is empty. Gray's heading gives no everyday name, and no source I opened gave one.
- No other field is blank. Each entry has type, joints and landmarks.

## Terminology changed from 1918 Gray's
- "semilunar notch" (greater sigmoid cavity) became trochlear notch (ulna, humerus).
- "musculospiral / radial sulcus" became radial groove (humerus).
- "navicular" (carpal) became scaphoid (radius, joints).
- "proximal radioulnar joint" (ulna): Gray's describes the radial notch receiving the radial head
  inside the elbow region. I used the modern joint name.

## Doubts and inferences
- Hip bone `type` = "flat": Gray's doc 17 lists the os coxae among flat bones, but doc 57 calls it
  "irregularly shaped". Many modern texts call it irregular. The owner should choose.
- Patella `type` = "sesamoid": Gray's doc 60 says it is usually regarded as sesamoid. Doc 17 notes
  that some authorities call it short or flat.
- Humerus tennis/golfer's elbow lines: NIAMS gives the conditions, and Gray's gives the
  epicondyle attachments of the common extensor and flexor tendons. Linking the two is my own synthesis.
- Humerus line "ulnar nerve runs behind the medial epicondyle" is anatomy rather than a condition.
  It is clinically relevant, but it could move to location/landmarks if the owner prefers.
- Radius wrist-fracture line: MedlinePlus says the wrist is two forearm bones plus carpals and that
  falls on an outstretched hand cause injuries. It does not name the radius (Gray's gives the
  radius-carpal joint), and it does not say distal radius fracture. Colles fracture is not in any source I opened.
- Ulna: the UCL injury (NIAMS) is tied to its attachments on the coronoid process and olecranon (Gray's).
  The olecranon bursa is from Gray's, and bursitis is in MedlinePlus's elbow list. I did not claim
  olecranon bursitis as a named condition.
- Hip bone clinical lines (dysplasia, osteoarthritis) are about the hip joint. That joint includes the acetabulum.
- No disease ids used; none of the allowed ids fit.

## URLs
- https://www.niams.nih.gov/health-topics/knee-problems returned 404 (not used).
- The NIAMS Knee Problems PDF on webharvest.gov downloaded but was unreadable (compressed PDF); not used.
- All cited URLs opened on the first try.
