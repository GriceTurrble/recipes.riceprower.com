#!/usr/bin/env ruby

require 'algolia'

def api_key
    return ENV["ALGOLIA_API_KEY"] if ENV["ALGOLIA_API_KEY"]

    key_file = File.join(File.dirname(__FILE__), '..', '_algolia_api_key')
    if File.exist?(key_file) && File.size(key_file).positive?
        return File.open(key_file).read.strip
    end

    print ">>> Error: ALGOLIA_API_KEY environment variable or _algolia_api_key required in repo root\n"
    exit 1
end

def app_id
    return ENV["ALGOLIA_APPLICATION_ID"] if ENV["ALGOLIA_APPLICATION_ID"]

    print ">>> Error: ALGOLIA_APPLICATION_ID environment variable required\n"
    exit 1
end

def index_name
    return ENV["ALGOLIA_INDEX"] if ENV["ALGOLIA_INDEX"]

    print ">>> Error: ALGOLIA_INDEX env var required\n"
    exit 1
end

# Initialize client and index
write_client = Algolia::Search::Client.create(app_id, api_key)
write_index = write_client.init_index(index_name)

# Clear all records
write_index.clear_objects()

print ">>> Records from index #{ index_name } successfully cleared.\n"
